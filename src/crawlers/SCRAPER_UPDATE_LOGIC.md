# Scraper Update Logic - Preserving Existing Data

##概念 (Concept)

Scraper używa inteligentnej logiki aktualizacji, która **nie nadpisuje** istniejących danych, jeśli nowe dane nie zostały znalezione. To zapobiega utracie wartościowych informacji podczas częściowo nieudanych scrapingów.

## Jak to działa?

### 1. Marker "NOT_FOUND"

LLM został poinstruowany aby zwracał dokładnie string `"NOT_FOUND"` dla każdego pola, którego informacji nie może znaleźć w scraped content.

```python
# W system prompt:
"If information is not available or unclear, use exactly this phrase: 'NOT_FOUND'"
```

### 2. Logika Merge

Podczas zapisywania danych:

```python
if new_value and new_value != "NOT_FOUND":
    # Aktualizuj pole nową wartością
    clean_data[field] = new_value
    updated_fields.append(field)
elif field in existing_data:
    # Zachowaj istniejącą wartość
    preserved_fields.append(field)
else:
    # Nowe pole, pusta wartość
    clean_data[field] = ""
```

### 3. Przykład Działania

**Istniejące dane** (`germany.json`):
```json
{
  "country_name": "Germany",
  "population": "84,000,000",
  "army_size": "183,000",
  "economic_strengths": "Automotive, machinery, chemicals"
}
```

**Nowy scraping** (znaleziono tylko population):
```json
{
  "country_name": "Germany",
  "population": "84,500,000",
  "army_size": "NOT_FOUND",
  "economic_strengths": "NOT_FOUND"
}
```

**Wynik** (merged):
```json
{
  "country_name": "Germany",
  "population": "84,500,000",        // ✅ Zaktualizowano
  "army_size": "183,000",            // 💾 Zachowano istniejące
  "economic_strengths": "Automotive, machinery, chemicals"  // 💾 Zachowano istniejące
}
```

## Logi

System loguje szczegółowe informacje o aktualizacji:

```
✅ Data saved to resources/germany.json
   📝 Updated fields (3): population, digitalization_level, political_economic_threats
   💾 Preserved existing data (5): army_size, economic_strengths, military_threats, development_milestones, key_bilateral_relations
```

## Korzyści

### ✅ Bezpieczne Częściowe Aktualizacje
- Można uruchamiać scraper wielokrotnie bez obawy o utratę danych
- Każdy scraping może dostarczyć informacje o różnych polach

### ✅ Incremental Data Collection
- Pierwsze uruchomienie: zbierz co się da
- Drugie uruchomienie: uzupełnij brakujące pola
- Trzecie uruchomienie: zaktualizuj przestarzałe dane

### ✅ Odporność na Błędy
- Jeśli jedna strona nie działa, inne dane są zachowane
- Problemy z siecią nie niszczą istniejących informacji

### ✅ Aktualizacje Selected Fields
- Można uruchomić scraper tylko dla konkretnych źródeł
- Zaktualizuje tylko te pola, które udało się zebrać

## Użycie

### Normalne uruchomienie (aktualizuje znalezione pola):
```bash
python3 src/crawlers/germany_advanced_scraper.py
```

### Sprawdzenie co zostało zaktualizowane:
Sprawdź logi - scraper pokazuje:
- Które pola zostały zaktualizowane
- Które pola zachowały starą wartość

### Wymuszone pełne nadpisanie (usuń stary plik):
```bash
rm resources/germany.json
python3 src/crawlers/germany_advanced_scraper.py
```

## Uwagi

### Empty vs NOT_FOUND

- `""` (pusty string): Pole nigdy nie miało wartości
- `"NOT_FOUND"`: Próbowano znaleźć, ale nie udało się (zachowaj stare dane)

### Lista (key_bilateral_relations)

Dla list logika jest podobna:
- Jeśli znaleziono nowe kraje → aktualizuj całą listę
- Jeśli zwrócono "NOT_FOUND" → zachowaj starą listę
- Jeśli pusta lista `[]` → zachowaj starą listę (prawdopodobnie nie znaleziono)

### country_name

Pole `country_name` zawsze powinno być aktualizowane (nie powinno być "NOT_FOUND").

## Best Practices

### 1. Pierwsze Uruchomienie
Upewnij się, że masz dobre podstawowe źródła danych.

### 2. Regularne Aktualizacje
Uruchamiaj scraper regularnie (np. raz w tygodniu) aby aktualizować dane.

### 3. Monitorowanie Logów
Zawsze sprawdzaj logi aby zobaczyć:
- Które pola zostały zaktualizowane
- Które pola zachowały stare wartości
- Czy są błędy podczas scrapingu

### 4. Backup
Przed znaczącymi zmianami w scraperze, zrób backup:
```bash
cp resources/germany.json resources/germany_backup_$(date +%Y%m%d).json
```

## Rozwiązywanie Problemów

### Problem: Wszystkie pola zwracają "NOT_FOUND"
**Rozwiązanie**: 
- Sprawdź czy strony są dostępne
- Sprawdź czy scraper poprawnie ekstrahuje tekst
- Sprawdź raw content (`germany_raw_content.json`)

### Problem: Stare dane są niepoprawne
**Rozwiązanie**:
- Ręcznie edytuj `germany.json`
- Lub usuń plik i uruchom scraper od nowa

### Problem: Chcę wymusić aktualizację konkretnego pola
**Rozwiązanie**:
- Ręcznie zmień wartość na pustą `""`
- Uruchom scraper - zapełni puste pole

## Przyszłe Ulepszenia

- [ ] Wersjonowanie danych (tracking zmian)
- [ ] Confidence score dla każdego pola
- [ ] Timestamp dla każdego pola (kiedy ostatnio aktualizowano)
- [ ] Automatyczne wykrywanie przestarzałych danych
- [ ] Web UI do przeglądu i ręcznej edycji danych
