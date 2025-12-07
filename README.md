# HackNation - System Prognozowania Geopolitycznego

System analizy geopolitycznej wykorzystujący Mesa framework i Google Gemini AI do generowania wyjaśnialnych prognoz dla krajów.

## 🚀 Szybki Start

### 1. Instalacja zależności

```bash
uv sync
```

### 2. Konfiguracja

Skopiuj przykładowy plik konfiguracyjny:

```bash
cp .env.example .env
```

Edytuj `.env` i dodaj swój klucz API Google:

```env
GEMINI_API_KEY=your_api_key_here
```

**Test konfiguracji:**

```bash
python3 test_config.py
```

### 3. Uruchomienie

```bash
python3 test2.py
```

📖 **Szczegółowy przewodnik**: Zobacz [QUICKSTART.md](QUICKSTART.md) dla zaawansowanych opcji konfiguracji.

## 🤖 Automatyczna Aktualizacja Danych

System automatycznie aktualizuje dane krajów:

- **Harmonogram**: Codziennie o 3:00 UTC
- **Źródła**: Oficjalne strony rządowe
- **Technologia**: GitHub Actions + LLM

### Ręczne uruchomienie:

```bash
# Przez GitHub Web UI
# Actions → "Update Germany Data" → Run workflow

# Przez GitHub CLI
gh workflow run "Update Germany Data"

# Aktualizacja wielu krajów
gh workflow run "Update All Countries Data" -f countries="germany,france"
```

📖 **Więcej informacji**: [ON_DEMAND_ACTIONS.md](ON_DEMAND_ACTIONS.md) - Kompletny przewodnik

## ⚙️ Konfiguracja

System używa pliku `.env` do konfiguracji wszystkich parametrów. Zobacz [CONFIG.md](CONFIG.md) dla szczegółowych informacji.

### Główne parametry:

- **GEMINI_MODEL_NAME**: Model AI (domyślnie: `gemini-2.0-flash`)
- **GEMINI_TEMPERATURE**: Kreatywność odpowiedzi (domyślnie: `0.2`)
- **GEMINI_MAX_TOKENS**: Maksymalna długość odpowiedzi (domyślnie: `4096`)
- **LOG_LEVEL**: Szczegółowość logów (domyślnie: `INFO`)
- **REPORT_DIR**: Katalog dla raportów PDF (domyślnie: `reports`)

Zobacz pełną dokumentację w [CONFIG.md](CONFIG.md).

## 📊 Funkcje

- **Multi-czynnikowa analiza scenariuszy**: 6 współzależnych czynników globalnych z wagami
- **Chain of Thought**: Pełna wyjaśnialność procesu analizy AI
- **Prognozy 12 i 36-miesięczne**: Pozytywne i negatywne scenariusze
- **Raporty PDF**: Profesjonalne raporty z analizami
- **System logowania**: Szczegółowe logi w plikach i konsoli
- **Web Scraping**: Automatyczne zbieranie danych o krajach z wiarygodnych źródeł

## 🕷️ Zbieranie Danych o Krajach

System umożliwia automatyczne zbieranie danych z oficjalnych źródeł:

```bash
# Scrape danych dla pojedynczego kraju
python3 scrape_country_data.py germany

# Scrape wszystkich krajów
python3 scrape_country_data.py --all
```

Zobacz [SCRAPER_GUIDE.md](SCRAPER_GUIDE.md) dla szczegółów.

## 📁 Struktura Projektu

```
hacknation/
├── src/
│   ├── agents/              # Agenci Mesa
│   │   ├── country_agent.py
│   │   └── forecasting_agent.py
│   ├── configuration.py     # System konfiguracji
│   └── report_generator.py  # Generator PDF
├── resources/               # Dane krajów (JSON)
├── logs/                    # Pliki logów
├── reports/                 # Raporty PDF
├── test2.py                 # Główny skrypt
└── .env                     # Konfiguracja (nie w git)
```

## 📖 Dokumentacja

- [CONFIG.md](CONFIG.md) - Szczegóły konfiguracji
- [CHAIN_OF_THOUGHT.md](CHAIN_OF_THOUGHT.md) - Wyjaśnialność AI
- [SCENARIO.md](SCENARIO.md) - Dokumentacja scenariuszy
- [WIELOCZYNNIKOWA_ANALIZA.md](WIELOCZYNNIKOWA_ANALIZA.md) - Analiza wieloczynnikowa

## 🛠️ Technologie

- **Mesa**: Framework do symulacji opartych na agentach
- **Google Gemini AI**: Generowanie prognoz
- **Pydantic**: Walidacja danych i konfiguracji
- **ReportLab**: Generowanie raportów PDF
- **Python 3.13+**

## 📝 Licencja

MIT
