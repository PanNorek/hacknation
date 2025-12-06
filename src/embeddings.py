"""
Moduł do generowania embeddingów i zapisu do PostgreSQL z pgvector.
"""
import os
from pathlib import Path
from sentence_transformers import SentenceTransformer
import numpy as np
from tqdm import tqdm
from db_config import db_config


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
        print(f"🧠 Ładowanie modelu embeddings: {model_name}...")
        self.model = SentenceTransformer(model_name)
        print(f"✅ Model załadowany! Wymiary wektora: {self.model.get_sentence_embedding_dimension()}\n")
    
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
        conn = db_config.get_connection()
        cursor = conn.cursor()
        
        try:
            # Generuj embedding ze STRESZCZENIA (nie z całego tekstu)
            embedding = self.generate_embedding(summary)
            
            # Konwertuj numpy array na listę Python dla pgvector
            embedding_list = embedding.tolist()
            
            # SQL: Wstaw nowy dokument lub zaktualizuj istniejący
            cursor.execute("""
                INSERT INTO documents (filename, raw_text, summary, embedding)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (filename) 
                DO UPDATE SET 
                    raw_text = EXCLUDED.raw_text,
                    summary = EXCLUDED.summary,
                    embedding = EXCLUDED.embedding,
                    updated_at = CURRENT_TIMESTAMP
            """, (filename, raw_text, summary, embedding_list))
            
            conn.commit()
            print(f"  ✓ {filename}")
            
        except Exception as e:
            conn.rollback()
            print(f"  ❌ Błąd: {str(e)}")
            raise
            
        finally:
            cursor.close()
            db_config.close_connection(conn)
    
    def process_documents(
        self, 
        extracted_dir: str = "data/extracted",
        summaries_dir: str = "data/summaries"
    ):
        """
        Przetwarza wszystkie dokumenty: generuje embeddingi i zapisuje do bazy.
        
        Args:
            extracted_dir: Folder z pełnymi tekstami
            summaries_dir: Folder ze streszczeniami
        """
        extracted_path = Path(extracted_dir)
        summaries_path = Path(summaries_dir)
        
        # Znajdź wszystkie streszczenia
        summary_files = list(summaries_path.glob("*_summary.txt"))
        
        if not summary_files:
            print(f"⚠️  Brak streszczeń w {summaries_dir}")
            print(f"💡 Najpierw uruchom: python src/summarizer.py")
            return
        
        print(f"🧠 Znaleziono {len(summary_files)} streszczeń do przetworzenia\n")
        
        success_count = 0
        
        for summary_file in tqdm(summary_files, desc="Generowanie embeddingów"):
            try:
                # Nazwa oryginału (bez _summary)
                original_name = summary_file.stem.replace("_summary", "")
                pdf_filename = f"{original_name}.pdf"
                
                # Ścieżka do pełnego tekstu
                extracted_file = extracted_path / f"{original_name}.txt"
                
                if not extracted_file.exists():
                    print(f"  ⚠️  Brak pliku: {extracted_file.name}")
                    continue
                
                # Wczytaj pełny tekst
                with open(extracted_file, 'r', encoding='utf-8') as f:
                    raw_text = f.read()
                
                # Wczytaj streszczenie
                with open(summary_file, 'r', encoding='utf-8') as f:
                    summary = f.read()
                
                # Zapisz do bazy z embeddingiem
                self.store_document(pdf_filename, raw_text, summary)
                success_count += 1
                
            except Exception as e:
                print(f"  ❌ Błąd przy {summary_file.name}: {str(e)}")
        
        print(f"\n✅ Zapisano {success_count}/{len(summary_files)} dokumentów do bazy")


def main():
    """Główna funkcja do uruchomienia z linii komend."""
    print("=" * 80)
    print("🧠 GENERATOR EMBEDDINGÓW + ZAPIS DO POSTGRES")
    print("=" * 80)
    print()
    
    # Inicjalizuj generator
    generator = EmbeddingGenerator()
    
    # Przetwarzaj dokumenty
    generator.process_documents()
    
    print("\n" + "=" * 80)
    print("✅ ZAKOŃCZONO ZAPISYWANIE DO BAZY")
    print("=" * 80)


if __name__ == "__main__":
    main()