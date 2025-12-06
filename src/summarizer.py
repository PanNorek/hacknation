"""
Moduł do lokalnego generowania streszczeń PDF używając modeli Hugging Face.
DARMOWE - działa bez API keys!
"""

import os
from pathlib import Path
from transformers import pipeline
from tqdm import tqdm


class LocalSummarizer:
    """
    Klasa do lokalnego generowania streszczeń używając modeli transformers.
    Używa modelu: facebook/bart-large-cnn (darmowy, lokalny)
    """

    def __init__(self, model_name: str = "facebook/bart-large-cnn"):
        """
        Inicjalizacja summarizera.

        Args:
            model_name: Nazwa modelu Hugging Face (domyślnie BART)
        """
        print(f"🤖 Ładowanie modelu summarization: {model_name}...")
        print("⏳ Pierwsze uruchomienie może zająć kilka minut (pobieranie modelu)...")

        self.summarizer = pipeline(
            "summarization", model=model_name, device=-1  # CPU (użyj 0 dla GPU)
        )

        print("✅ Model załadowany!\n")

    def summarize_text(
        self, text: str, max_length: int = 150, min_length: int = 50
    ) -> str:
        """
        Generuje streszczenie tekstu.

        Args:
            text: Tekst do streszczenia
            max_length: Maksymalna długość streszczenia (w tokenach)
            min_length: Minimalna długość streszczenia (w tokenach)

        Returns:
            Wygenerowane streszczenie
        """
        # BART ma limit ~1024 tokeny, więc obcinamy długi tekst
        max_input_length = 1024

        # Przybliżenie: 1 token ≈ 4 znaki
        if len(text) > max_input_length * 4:
            text = text[: max_input_length * 4]
            print(f"  ⚠️  Tekst został obcięty do {max_input_length * 4} znaków")

        # Generuj streszczenie
        summary = self.summarizer(
            text, max_length=max_length, min_length=min_length, do_sample=False
        )

        return summary[0]["summary_text"]

    def process_directory(
        self, input_dir: str = "data/extracted", output_dir: str = "data/summaries"
    ):
        """
        Przetwarza wszystkie pliki .txt z folderu extracted i generuje streszczenia.

        Args:
            input_dir: Folder z wyekstraktowanymi tekstami
            output_dir: Folder na streszczenia
        """
        input_path = Path(input_dir)
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        # Znajdź wszystkie pliki .txt
        txt_files = list(input_path.glob("*.txt"))

        if not txt_files:
            print(f"⚠️  Brak plików .txt w {input_dir}")
            print(f"💡 Najpierw uruchom: python src/pdf_processor.py")
            return

        print(f"📝 Znaleziono {len(txt_files)} plików do streszczenia\n")

        # Przetwarzaj każdy plik
        for txt_file in tqdm(txt_files, desc="Generowanie streszczeń"):
            try:
                # Wczytaj tekst
                with open(txt_file, "r", encoding="utf-8") as f:
                    text = f.read()

                # Pomiń puste pliki
                if len(text.strip()) < 100:
                    print(f"  ⚠️  {txt_file.name} - tekst za krótki, pomijam")
                    continue

                # Generuj streszczenie
                print(f"\n  📄 Przetwarzanie: {txt_file.name}")
                summary = self.summarize_text(text)

                # Zapisz streszczenie
                summary_file = output_path / f"{txt_file.stem}_summary.txt"
                with open(summary_file, "w", encoding="utf-8") as f:
                    f.write(summary)

                print(f"  ✓ Zapisano: {summary_file.name}")
                print(f"  📊 Długość streszczenia: {len(summary)} znaków")

            except Exception as e:
                print(f"  ❌ Błąd przy przetwarzaniu {txt_file.name}: {str(e)}")

        print(f"\n✅ Gotowe! Streszczenia zapisane w: {output_dir}")


def main():
    """Główna funkcja do uruchomienia z linii komend."""
    print("=" * 80)
    print("📝 GENERATOR STRESZCZEŃ (LOKALNY - DARMOWY)")
    print("=" * 80)
    print()

    # Inicjalizuj summarizer
    summarizer = LocalSummarizer()

    # Przetwarzaj pliki
    summarizer.process_directory()

    print("\n" + "=" * 80)
    print("✅ ZAKOŃCZONO GENEROWANIE STRESZCZEŃ")
    print("=" * 80)


if __name__ == "__main__":
    main()
