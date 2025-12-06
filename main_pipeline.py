"""
Główny pipeline przetwarzania dokumentów PDF.
"""
import sys
from pathlib import Path

# Dodaj src do PYTHONPATH
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.pdf_processor import PDFProcessor
from summarizer import LocalSummarizer
from embeddings import EmbeddingGenerator


def main():
    """
    Główny pipeline:
    1. Ekstrakcja tekstu z PDF
    2. Generowanie streszczeń (LOCAL - DARMOWE)
    3. Generowanie embeddingów i zapis do Postgres
    """
    print("\n" + "="*80)
    print("🚀 PIPELINE PRZETWARZANIA DOKUMENTÓW PDF")
    print("="*80)
    print()
    
    try:
        # ============================================
        # KROK 1: Ekstrakcja tekstu z PDF
        # ============================================
        print("="*80)
        print("📄 KROK 1: Ekstrakcja tekstu z PDF")
        print("="*80)
        print()
        
        processor = PDFProcessor()
        extracted_count = processor.process_directory()
        
        if extracted_count == 0:
            print("\n⚠️  Brak plików PDF do przetworzenia!")
            print("💡 Dodaj pliki PDF do folderu: data/pdfs/")
            return
        
        print(f"\n✅ Wyekstraktowano {extracted_count} dokumentów")
        
        # ============================================
        # KROK 2: Generowanie streszczeń (LOCAL)
        # ============================================
        print("\n" + "="*80)
        print("📝 KROK 2: Generowanie streszczeń (LOKALNIE - DARMOWE)")
        print("="*80)
        print()
        
        summarizer = LocalSummarizer()
        summarizer.process_directory()
        
        # ============================================
        # KROK 3: Embeddings + zapis do Postgres
        # ============================================
        print("\n" + "="*80)
        print("🧠 KROK 3: Generowanie embeddingów i zapis do bazy")
        print("="*80)
        print()
        
        generator = EmbeddingGenerator()
        generator.process_documents()
        
        # ============================================
        # PODSUMOWANIE
        # ============================================
        print("\n" + "="*80)
        print("✅ PIPELINE ZAKOŃCZONY POMYŚLNIE!")
        print("="*80)
        print()
        print("📊 Co dalej?")
        print("  • Sprawdź bazę: python check_database.py")
        print("  • Testuj wyszukiwanie: python src/search.py")
        print("  • Dodaj więcej PDF do data/pdfs/ i uruchom ponownie")
        print()
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Pipeline przerwany przez użytkownika")
        sys.exit(1)
        
    except Exception as e:
        print(f"\n\n❌ BŁĄD: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()