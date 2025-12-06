# Szybki Start - Konfiguracja

## 1. Podstawowa Konfiguracja

### Krok 1: Skopiuj plik przykładowy
```bash
cp .env.example .env
```

### Krok 2: Dodaj klucz API
Edytuj plik `.env` i dodaj swój klucz:
```env
GEMINI_API_KEY=twoj_klucz_api_tutaj
```

### Krok 3: Uruchom test
```bash
python3 test_config.py
```

Jeśli widzisz "✅ Configuration loaded successfully!" - jesteś gotowy!

---

## 2. Dostosowywanie Konfiguracji

### Zmiana Modelu AI

Domyślnie używany jest `gemini-2.0-flash` (szybki, ekonomiczny).

**Dla lepszej jakości** (wolniejszy, droższy):
```env
GEMINI_MODEL_NAME=gemini-1.5-pro
GEMINI_MAX_TOKENS=8192
```

**Dla większej kreatywności**:
```env
GEMINI_TEMPERATURE=0.5
```

⚠️ **Uwaga**: Wyższa temperatura (>0.5) może zmniejszyć spójność prognoz.

---

### Zmiana Poziomu Logowania

**Debug (wszystkie szczegóły)**:
```env
LOG_LEVEL=DEBUG
```

**Tylko błędy**:
```env
LOG_LEVEL=ERROR
```

**Opcje**: DEBUG, INFO, WARNING, ERROR

---

### Zmiana Lokalizacji Plików

**Własne katalogi**:
```env
LOG_DIR=output/logs
REPORT_DIR=output/reports
```

System automatycznie utworzy te katalogi.

---

### Więcej Krajów w Kontekście

Domyślnie analizowane są 5 innych krajów dla oszczędności tokenów.

**Zwiększ limit**:
```env
MAX_OTHER_COUNTRIES_CONTEXT=10
```

⚠️ **Uwaga**: Więcej krajów = więcej tokenów = wyższe koszty API.

---

## 3. Przykładowe Konfiguracje

### Konfiguracja Produkcyjna (MSZ)
```env
GEMINI_API_KEY=your_key_here
GEMINI_MODEL_NAME=gemini-2.0-flash
GEMINI_TEMPERATURE=0.2
GEMINI_MAX_TOKENS=4096
LOG_LEVEL=INFO
REPORT_DIR=/shared/reports
MAX_OTHER_COUNTRIES_CONTEXT=8
```

### Konfiguracja Rozwojowa
```env
GEMINI_API_KEY=your_key_here
GEMINI_MODEL_NAME=gemini-2.0-flash
GEMINI_TEMPERATURE=0.2
GEMINI_MAX_TOKENS=4096
LOG_LEVEL=DEBUG
LOG_DIR=dev_logs
REPORT_DIR=dev_reports
MAX_OTHER_COUNTRIES_CONTEXT=3
```

### Konfiguracja Eksperymentalna
```env
GEMINI_API_KEY=your_key_here
GEMINI_MODEL_NAME=gemini-1.5-pro
GEMINI_TEMPERATURE=0.5
GEMINI_MAX_TOKENS=8192
LOG_LEVEL=DEBUG
MAX_OTHER_COUNTRIES_CONTEXT=10
```

---

## 4. Rozwiązywanie Problemów

### Błąd: "GOOGLE_API_KEY environment variable is not set"

**Rozwiązanie**:
1. Sprawdź czy plik `.env` istnieje: `ls -la .env`
2. Sprawdź czy zawiera klucz: `grep GEMINI_API_KEY .env`
3. Jeśli nie, dodaj: `echo "GEMINI_API_KEY=your_key" >> .env`

### Błąd: Permission denied dla katalogów

**Rozwiązanie**:
```bash
chmod 755 logs reports
```

### Logi są zbyt szczegółowe

**Rozwiązanie**:
```env
LOG_LEVEL=WARNING
```

### Raporty są za duże

**Rozwiązanie**:
```env
MAX_OTHER_COUNTRIES_CONTEXT=3
GEMINI_MAX_TOKENS=2048
```

---

## 5. Weryfikacja Konfiguracji

Zawsze po zmianie `.env` uruchom test:

```bash
python3 test_config.py
```

To pokaże wszystkie aktywne ustawienia.

---

## 6. Bezpieczeństwo

✅ **DO**:
- Przechowuj `.env` lokalnie
- Używaj `.env.example` jako szablonu
- Rotuj klucze API regularnie

❌ **NIE COMMITUJ**:
- Pliku `.env` do gita
- Kluczy API w kodzie
- Wrażliwych danych w raportach

---

## Więcej Informacji

- [CONFIG.md](CONFIG.md) - Pełna dokumentacja
- [README.md](README.md) - Przegląd projektu
- [CHANGELOG.md](CHANGELOG.md) - Historia zmian
