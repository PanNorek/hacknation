"""
Moduł do generowania embeddingów i zapisu do PostgreSQL z pgvector.
"""

from pathlib import Path
from sentence_transformers import SentenceTransformer
import numpy as np
from tqdm import tqdm
from src.db.db_config import db_config
from src.db.hack.embeddings import Embedding


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

    def generate_embedding(self, text: str) -> np.ndarray:
        """
        Generuje embedding dla tekstu.

        Args:
            text: Tekst do zakodowania

        Returns:
            Wektor embedding (numpy array)
        """
        return self.model.encode(text, convert_to_numpy=True)

    def store_document(self, filename: str, raw_text: str, summary: str):
        """
        Zapisuje dokument wraz z embeddingiem w PostgreSQL.

        Args:
            filename: Nazwa pliku PDF
            raw_text: Pełny wyekstraktowany tekst
            summary: Wygenerowane streszczenie
        """
        sessionmaker = db_config.get_sessionmaker()

        with sessionmaker() as sess:
            embedding = self.generate_embedding(summary)
            embedding_list = embedding.tolist()
            sess.add(
                Embedding(
                    content=summary,
                    embedding=embedding_list,
                    meta_data={},
                )
            )
            sess.commit()

    def process_documents(
        self,
        extracted_dir: str = "data/extracted",
        summaries_dir: str = "data/summaries",
    ):
        """
        Przetwarza wszystkie dokumenty: generuje embeddingi i zapisuje do bazy.

        Args:
            extracted_dir: Folder z pełnymi tekstami
            summaries_dir: Folder ze streszczeniami
        """
        extracted_path = Path(extracted_dir)
        summaries_path = Path(summaries_dir)

        summary_files = list(summaries_path.glob("*_summary.txt"))

        if not summary_files:
            print(f"No summaries found in {summaries_dir}")
            print(f"Run: python src/summarizer.py")
            return

        print(f"Found {len(summary_files)} summaries to process\n")

        success_count = 0

        for summary_file in tqdm(summary_files, desc="Generating embeddings"):
            try:
                # Original name (without _summary)
                original_name = summary_file.stem.replace("_summary", "")
                pdf_filename = f"{original_name}.pdf"

                # Path to full text
                extracted_file = extracted_path / f"{original_name}.txt"

                if not extracted_file.exists():
                    print(f"No file found: {extracted_file.name}")
                    continue

                with open(extracted_file, "r", encoding="utf-8") as f:
                    raw_text = f.read()

                with open(summary_file, "r", encoding="utf-8") as f:
                    summary = f.read()

                self.store_document(pdf_filename, raw_text, summary)
                success_count += 1

            except Exception as e:
                print(f"Error: {summary_file.name}: {str(e)}")

        print(
            f"\nSuccessfully stored {success_count}/{len(summary_files)} documents to database"
        )
