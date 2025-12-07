"""
Moduł do generowania embeddingów i zapisu do PostgreSQL z pgvector.
"""

import asyncio
import asyncpg
from typing import List, Dict
from pathlib import Path
from sentence_transformers import SentenceTransformer
import numpy as np
from tqdm import tqdm
from src.db.db_config import db_config
from src.db.hack.embeddings import Embedding
from src.pdf_processor import PDFProcessor


class EmbeddingGenerator:
    """
    Klasa do generowania embeddingów używając sentence-transformers.
    """

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Inicjalizacja generatora embeddingów.

        Args:
            model_name: Nazwa modelu sentence-transformers (384 wymiary)
        """
        self.model = SentenceTransformer(model_name)

    async def generate_embedding(self, text: str) -> np.ndarray:
        """
        Generuje embedding dla tekstu.

        Args:
            text: Tekst do zakodowania

        Returns:
            Wektor embedding (numpy array)
        """
        return self.model.encode(text, convert_to_numpy=True)

    async def store_document(self, content: str):
        """
        Zapisuje dokument wraz z embeddingiem w PostgreSQL.

        Args:
            filename: Nazwa pliku PDF
            page_text: Tekst z jednej strony PDF
            summary: Wygenerowane streszczenie
        """
        sessionmaker = db_config.get_sessionmaker()

        async with sessionmaker() as a_sess:
            embedding = await self.generate_embedding(content)
            embedding_list = embedding.tolist()
            a_sess.add(
                Embedding(
                    content=content,
                    embedding=embedding_list,
                    meta_data={},
                )
            )
            await a_sess.commit()

    async def process_documents(
        self,
        pdfs_dir: str = "data/pdfs",
    ):
        """
        Przetwarza wszystkie dokumenty: generuje embeddingi i zapisuje do bazy.

        Args:
            extracted_dir: Folder z pełnymi tekstami
            summaries_dir: Folder ze streszczeniami
        """
        pdfs_path = Path(pdfs_dir)
        pdf_files = list(pdfs_path.glob("*.pdf"))

        if not pdf_files:
            print(f"No PDFs found in {pdfs_dir}")
            return

        print(f"Found {len(pdf_files)} PDFs to process\n")

        success_count = 0
        count = 0

        for pdf_file in pdf_files:
            try:
                pdf_processor = PDFProcessor()
                pages = pdf_processor.extract_text_from_pdfs_by_page(pdf_file)
                count += len(pages)
                for page_text in tqdm(pages, desc="Generating embeddings"):
                    await self.store_document(page_text)
                    success_count += 1

            except Exception as e:
                print(f"Error: {pdf_file.name}: {str(e)}")

        print(f"\nSuccessfully stored {success_count}/{count} documents to database")


from src.configuration import Configuration
from src.db.db_config import db_config


class EmbeddingStore:
    def __init__(self):
        self.config = Configuration()
        self.pool = None  # asyncpg pool

    async def init(self):
        """Initialize asyncpg pool once."""
        self.pool = await db_config.get_pool()

    async def search(self, query: str, top_k: int = 3) -> List[Dict]:
        if self.pool is None:
            raise RuntimeError("Call await store.init() before using search()")

        generator = EmbeddingGenerator()

        # 1) Generate vector
        query_embedding = await generator.generate_embedding(query)
        query_embedding = query_embedding.tolist()

        # 2) Convert to pgvector format
        vector_str = "[" + ",".join(str(v) for v in query_embedding) + "]"

        sql = """
        SELECT 
            id,
            content,
            meta_data,
            created_at,
            1 - (embedding <#> $1) AS similarity
        FROM embeddings
        ORDER BY embedding <#> $1
        LIMIT $2;
        """

        async with self.pool.acquire() as conn:
            rows = await conn.fetch(sql, vector_str, top_k)

        return [dict(r) for r in rows]
