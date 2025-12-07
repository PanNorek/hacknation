"""
Moduł do ekstrakcji tekstu z plików PDF.
"""

import re
from pathlib import Path
from pypdf import PdfReader
from typing import List
from tqdm import tqdm


class PDFProcessor:
    """
    Klasa do przetwarzania plików PDF i ekstrakcji tekstu.
    """

    def __init__(self, pdf_dir: str = "data/pdfs", output_dir: str = "data/extracted"):
        """
        Inicjalizacja processora PDF.

        Args:
            pdf_dir: Folder z plikami PDF do przetworzenia
            output_dir: Folder na wyekstraktowane teksty
        """
        self.pdf_dir = Path(pdf_dir)
        self.output_dir = Path(output_dir)

        # Utwórz foldery jeśli nie istnieją
        self.pdf_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def extract_text_from_pdf(self, pdf_path: Path) -> str:
        """
        Ekstraktuje tekst z pojedynczego pliku PDF.

        Args:
            pdf_path: Ścieżka do pliku PDF

        Returns:
            Wyekstraktowany tekst
        """
        try:
            reader = PdfReader(pdf_path)
            text = ""

            for page in reader.pages:
                text += page.extract_text() + "\n"

            return text.strip()

        except Exception as e:
            raise Exception(f"Błąd podczas czytania {pdf_path.name}: {str(e)}")

    def extract_text_from_pdfs_by_page(self, pdf_path: Path) -> List[str]:
        """Page iterator for PDF file."""
        reader = PdfReader(pdf_path)
        cleaned_pages = []

        for page in reader.pages:
            raw = page.extract_text() or ""
            cleaned = re.sub(r"\s+", " ", raw).strip()
            cleaned_pages.append(cleaned)

        return cleaned_pages

    def process_directory(self) -> int:
        """
        Przetwarza wszystkie pliki PDF z folderu pdf_dir.

        Returns:
            Liczba przetworzonych plików
        """
        # Znajdź wszystkie pliki PDF
        pdf_files = list(self.pdf_dir.glob("*.pdf"))

        if not pdf_files:
            print(f"⚠️  Brak plików PDF w {self.pdf_dir}")
            return 0

        print(f"📄 Znaleziono {len(pdf_files)} plików PDF\n")

        success_count = 0

        for pdf_file in tqdm(pdf_files, desc="Ekstrakcja tekstu"):
            try:
                # Ekstraktuj tekst
                text = self.extract_text_from_pdf(pdf_file)

                # Pomiń puste pliki
                if len(text.strip()) < 50:
                    print(f"  ⚠️  {pdf_file.name} - zbyt mało tekstu, pomijam")
                    continue

                # Zapisz do pliku txt
                output_file = self.output_dir / f"{pdf_file.stem}.txt"
                with open(output_file, "w", encoding="utf-8") as f:
                    f.write(text)

                print(f"  ✓ {pdf_file.name} -> {output_file.name}")
                success_count += 1

            except Exception as e:
                print(f"  ❌ Błąd: {pdf_file.name} - {str(e)}")

        print(f"\n✅ Przetworzono {success_count}/{len(pdf_files)} plików")
        return success_count


def main():
    """Główna funkcja do uruchomienia z linii komend."""
    print("=" * 80)
    print("📄 EKSTRAKTOR TEKSTU Z PDF")
    print("=" * 80)
    print()

    processor = PDFProcessor()
    processor.process_directory()

    print("\n" + "=" * 80)
    print("✅ ZAKOŃCZONO EKSTRAKCJĘ")
    print("=" * 80)


if __name__ == "__main__":
    main()
