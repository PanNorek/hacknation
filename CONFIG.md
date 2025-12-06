# Konfiguracja Systemu Prognozowania Geopolitycznego

## Przegląd

System używa pliku `.env` do przechowywania wszystkich parametrów konfiguracyjnych. To pozwala na łatwe dostosowanie zachowania systemu bez modyfikacji kodu.

## Plik Konfiguracyjny

Skopiuj `.env.example` do `.env` i dostosuj wartości:

```bash
cp .env.example .env
```

## Parametry Konfiguracyjne

### Klucze API

| Parametr              | Opis                    | Wymagany | Domyślna wartość |
| --------------------- | ----------------------- | -------- | ---------------- |
| `GOOGLE_API_KEY`      | Klucz API Google Gemini | ✅ Tak   | -                |
| `GEMINI_API_KEY`      | Alternatywny klucz API  | Nie      | -                |
| `GEMINI_PROJECT_NAME` | Nazwa projektu Google   | Nie      | -                |

### Konfiguracja Modelu Gemini

| Parametr             | Opis                                   | Domyślna wartość   |
| -------------------- | -------------------------------------- | ------------------ |
| `GEMINI_MODEL_NAME`  | Nazwa modelu Gemini                    | `gemini-2.0-flash` |
| `GEMINI_TEMPERATURE` | Temperatura dla generowania (0.0-1.0)  | `0.2`              |
| `GEMINI_MAX_TOKENS`  | Maksymalna liczba tokenów w odpowiedzi | `4096`             |

**Uwagi:**

- **Temperature**: Niska wartość (0.2) zapewnia bardziej deterministyczne i spójne prognozy. Wyższa wartość (0.8-1.0) zwiększa kreatywność, ale może zmniejszyć spójność.
- **Model**: Dostępne modele:
  - `gemini-2.0-flash` - szybki, zoptymalizowany
  - `gemini-1.5-pro` - bardziej zaawansowany
  - `gemini-1.5-flash` - starszy model flash

### Konfiguracja Logowania

| Parametr    | Opis                                           | Domyślna wartość |
| ----------- | ---------------------------------------------- | ---------------- |
| `LOG_LEVEL` | Poziom logowania (DEBUG, INFO, WARNING, ERROR) | `INFO`           |
| `LOG_DIR`   | Katalog dla plików logów                       | `logs`           |

**Poziomy logowania:**

- `DEBUG`: Wszystkie szczegóły, w tym debugowanie AI
- `INFO`: Główne informacje o przebiegu symulacji
- `WARNING`: Ostrzeżenia
- `ERROR`: Tylko błędy

### Konfiguracja Raportów

| Parametr           | Opis                           | Domyślna wartość |
| ------------------ | ------------------------------ | ---------------- |
| `REPORT_DIR`       | Katalog dla raportów PDF       | `reports`        |
| `REPORT_PAGE_SIZE` | Rozmiar strony (A4 lub letter) | `A4`             |

### Konfiguracja Symulacji

| Parametr                      | Opis                                  | Domyślna wartość |
| ----------------------------- | ------------------------------------- | ---------------- |
| `MAX_OTHER_COUNTRIES_CONTEXT` | Maksymalna liczba krajów w kontekście | `5`              |

## Przykłady Użycia

### Zwiększenie szczegółowości logów

```env
LOG_LEVEL=DEBUG
```

### Użycie bardziej kreatywnego modelu

```env
GEMINI_MODEL_NAME=gemini-1.5-pro
GEMINI_TEMPERATURE=0.5
GEMINI_MAX_TOKENS=8192
```

### Zmiana formatu raportu

```env
REPORT_PAGE_SIZE=letter
REPORT_DIR=output/reports
```

### Więcej kontekstu krajów w analizie

```env
MAX_OTHER_COUNTRIES_CONTEXT=10
```

## Użycie w Kodzie

Konfiguracja jest automatycznie ładowana przez klasę `Configuration`:

```python
from src.configuration import Configuration

config = Configuration()

# Dostęp do parametrów
print(config.gemini_model_name)
print(config.gemini_temperature)
print(config.log_level)
```

## Bezpieczeństwo

⚠️ **WAŻNE**:

- **NIE** commituj pliku `.env` do repozytorium Git
- Plik `.env` jest już w `.gitignore`
- Używaj `.env.example` jako szablonu
- Przechowuj klucze API bezpiecznie

## Walidacja

System automatycznie waliduje konfigurację przy starcie:

- Sprawdza czy `GOOGLE_API_KEY` jest ustawiony
- Konwertuje typy (str → int, float)
- Stosuje wartości domyślne jeśli parametr nie jest ustawiony

## Troubleshooting

### "GOOGLE_API_KEY environment variable is not set"

Rozwiązanie:

```bash
echo "GOOGLE_API_KEY=your_actual_key" >> .env
```

### Logs nie są zapisywane

Sprawdź:

1. Czy katalog `LOG_DIR` istnieje (jest tworzony automatycznie)
2. Czy masz uprawnienia do zapisu
3. Czy `LOG_LEVEL` jest poprawny (DEBUG, INFO, WARNING, ERROR)

### Model nie działa

Sprawdź:

1. Czy nazwa modelu jest poprawna (`GEMINI_MODEL_NAME`)
2. Czy masz dostęp do tego modelu w swoim projekcie Google
3. Sprawdź logi pod kątem komunikatów błędów
