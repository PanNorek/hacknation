# Changelog

## [Unreleased] - 2024-12-06

### Added
- **Centralny system konfiguracji** (`src/configuration.py`)
  - Wszystkie parametry w jednym miejscu
  - Wsparcie dla pliku `.env`
  - Automatyczna walidacja typów przez Pydantic
  - Wartości domyślne dla wszystkich parametrów

- **Nowe parametry konfiguracyjne**:
  - `GEMINI_MODEL_NAME` - wybór modelu AI (domyślnie: gemini-2.0-flash)
  - `GEMINI_TEMPERATURE` - kontrola kreatywności (domyślnie: 0.2)
  - `GEMINI_MAX_TOKENS` - limit tokenów odpowiedzi (domyślnie: 4096)
  - `LOG_LEVEL` - poziom logowania (domyślnie: INFO)
  - `LOG_DIR` - katalog logów (domyślnie: logs)
  - `REPORT_DIR` - katalog raportów (domyślnie: reports)
  - `REPORT_PAGE_SIZE` - rozmiar strony PDF (domyślnie: A4)
  - `MAX_OTHER_COUNTRIES_CONTEXT` - limit krajów w kontekście (domyślnie: 5)

- **System logowania**
  - Zastąpiono wszystkie `print()` przez `logger.info/debug/warning/error()`
  - Logi zapisywane do plików z timestamp
  - Jednoczesne logowanie do konsoli i pliku
  - Konfigurowalny poziom logowania

- **Generator raportów PDF**
  - Klasa `ForecastReportGenerator`
  - Profesjonalne formatowanie z ReportLab
  - Strona tytułowa ze scenariuszem
  - Sekcje Chain of Thought dla każdego kraju
  - Tabele prognoz z kolorami
  - Metoda `generate_report()` do kompletnych raportów

- **Dokumentacja**
  - `CONFIG.md` - szczegółowa dokumentacja konfiguracji
  - `.env.example` - szablon pliku konfiguracyjnego
  - Zaktualizowano `README.md` z informacjami o konfiguracji
  - `test_config.py` - skrypt testowy konfiguracji

### Changed
- **forecasting_agent.py**
  - Używa `Configuration` zamiast hardcoded wartości
  - Model, temperatura i max_tokens z konfiguracji
  - Limit krajów w kontekście z konfiguracji

- **test2.py**
  - Używa `Configuration` dla wszystkich parametrów
  - Automatyczne tworzenie katalogów logs i reports
  - Integracja z generatorem PDF
  - Zbieranie i zapisywanie wszystkich prognoz do PDF

- **report_generator.py**
  - Używa `Configuration` dla parametrów raportów
  - Rozmiar strony z konfiguracji (A4/letter)
  - Katalog raportów z konfiguracji

### Fixed
- Kompatybilność z `GOOGLE_API_KEY` i `GEMINI_API_KEY`
- Dodano `extra = "ignore"` w Configuration aby ignorować nieużywane pola z .env

### Technical Details
- Pydantic Settings dla type-safe konfiguracji
- Environment variables z fallback do wartości domyślnych
- Centralizacja wszystkich "magic numbers" i stringów
- Łatwiejsza konfiguracja bez modyfikacji kodu

## [Previous] - Before Configuration System

### Features
- Mesa framework dla symulacji agentowych
- Gemini AI dla generowania prognoz
- Analiza wieloczynnikowa (6 współzależnych czynników)
- Chain of Thought wyjaśnialność
- Prognozy 12 i 36-miesięczne
- Dane krajów w JSON
- Jupyter notebooks dla eksploracji
