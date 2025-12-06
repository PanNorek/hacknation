# System Zbierania Danych o Krajach (Web Scraping)

## Przegląd

System automatycznego zbierania danych o krajach z wiarygodnych źródeł internetowych wykorzystując Scrapy framework.

## Struktura

```
src/country_scrapper/
├── spiders/
│   ├── base_country_spider.py   # Bazowy szablon dla wszystkich krajów
│   ├── germany_spider.py        # Spider dla Niemiec
│   └── [inne_kraje]_spider.py   # Spidery dla innych krajów
scrape_country_data.py           # Skrypt uruchomieniowy
```

## Funkcje

### 1. Automatyczne Zbieranie Danych

Spider automatycznie ekstrahuje:
- **Populację** - liczba mieszkańców
- **Siły zbrojne** - wielkość armii
- **Mocne strony gospodarcze** - kluczowe sektory
- **Poziom cyfryzacji** - infrastruktura technologiczna
- **Geografia** - położenie, granice, cechy geograficzne
- **Klimat** - typ klimatu
- **Waluta** - oficjalna waluta
- **Relacje bilateralne** - kluczowi partnerzy
- **Zagrożenia** - polityczne, ekonomiczne, militarne
- **Kamienie milowe** - ważne wydarzenia historyczne

### 2. Wiarygodne Źródła

Dla każdego kraju używane są oficjalne źródła:
- Strony rządowe (ministerstwa, urzędy statystyczne)
- Oficjalne portale krajowe
- CIA World Factbook (dla weryfikacji)
- Międzynarodowe organizacje (UN, NATO, EU)

### 3. Inteligentna Ekstrakcja

- **Wiele wzorców** - różne formaty danych
- **Kontekstowa analiza** - szukanie słów kluczowych w odpowiednim kontekście
- **Agregacja** - zbieranie danych z wielu źródeł
- **Walidacja** - sprawdzanie spójności
- **Fallback** - wartości domyślne jeśli dane nie zostały znalezione

## Użycie

### Instalacja Scrapy

```bash
pip install scrapy beautifulsoup4
```

### Scraping Pojedynczego Kraju

```bash
python3 scrape_country_data.py germany
```

### Scraping Wszystkich Krajów

```bash
python3 scrape_country_data.py --all
```

### Wyjście

Dane są zapisywane do `resources/[kraj].json` w formacie zgodnym z systemem prognozowania:

```json
{
  "country_name": "Germany",
  "geographical_features": "Central Europe; borders 9 countries",
  "population": "83 million",
  "climate": "Temperate seasonal climate",
  "economic_strengths": "automotive, engineering, chemical, renewable energy",
  "army_size": "183,000 active personnel",
  "digitalization_level": "Advanced: 5G, broadband, e-government",
  "currency": "Euro (EUR)",
  "key_bilateral_relations": ["France", "Poland", "USA", "UK"],
  "political_economic_threats": ["energy dependence", "supply chain risks"],
  "military_threats": ["cyber threats", "hybrid warfare"],
  "development_milestones": ["EU founding member (1957)", "NATO since 1955"]
}
```

## Tworzenie Nowego Spidera

### Metoda 1: Dziedziczenie z BaseCountrySpider

```python
from src.country_scrapper.spiders.base_country_spider import BaseCountrySpider

class PolandSpider(BaseCountrySpider):
    name = "poland_info"
    country_name = "Poland"
    start_urls = [
        "https://www.gov.pl/web/diplomacy",
        "https://www.gov.pl/web/national-defence",
        "https://stat.gov.pl/en/",
        "https://www.cia.gov/the-world-factbook/countries/poland/",
    ]
    
    def finalize_data(self):
        """Poland-specific defaults"""
        super().finalize_data()
        
        if not self.country_data["population"]:
            self.country_data["population"] = "~38 million"
        
        if not self.country_data["currency"]:
            self.country_data["currency"] = "Polish Złoty (PLN)"
```

### Metoda 2: Dostosowanie Istniejącego Spidera

Skopiuj `germany_spider.py` i dostosuj:
1. Zmień `name` i `country_name`
2. Zaktualizuj `start_urls` na strony docelowego kraju
3. Dostosuj `finalize_data()` z domyślnymi wartościami
4. Opcjonalnie: dodaj specyficzne wzorce ekstrakcji

## Najlepsze Praktyki

### 1. Wybór Źródeł

✅ **Dobre źródła:**
- Oficjalne strony rządowe (.gov, .gouv, .gob)
- Urzędy statystyczne
- Ministerstwa (obrony, spraw zagranicznych, gospodarki)
- CIA World Factbook
- UN, World Bank, IMF

❌ **Unikaj:**
- Wikipedia (niestabilne, często zmieniane)
- Blogi i media społecznościowe
- Strony bez weryfikacji
- Źródła w nieznanych językach bez tłumaczenia

### 2. Politeness Policy

```python
custom_settings = {
    'DOWNLOAD_DELAY': 2,  # 2 sekundy między requestami
    'CONCURRENT_REQUESTS_PER_DOMAIN': 1,  # Jeden request na raz
    'ROBOTSTXT_OBEY': True,  # Przestrzegaj robots.txt
}
```

### 3. Obsługa Błędów

Spider automatycznie:
- Loguje błędy połączeń
- Używa wartości domyślnych jeśli dane nie zostały znalezione
- Kontynuuje pracę nawet jeśli jedna strona zawiedzie

### 4. Walidacja Danych

Po scrapingu sprawdź:
```bash
cat resources/germany.json | python -m json.tool
```

## Struktura Danych

### Wymagane Pola

Każdy plik JSON musi zawierać:
- `country_name` - nazwa kraju
- `geographical_features` - cechy geograficzne
- `population` - liczba ludności
- `climate` - typ klimatu
- `economic_strengths` - mocne strony gospodarki
- `army_size` - wielkość sił zbrojnych
- `digitalization_level` - poziom cyfryzacji
- `currency` - waluta
- `key_bilateral_relations` - lista krajów-partnerów
- `political_economic_threats` - lista zagrożeń
- `military_threats` - lista zagrożeń militarnych
- `development_milestones` - lista kamieni milowych

### Formatowanie

- **Teksty**: Zwięzłe, max 200 znaków
- **Listy**: 3-8 elementów
- **Liczby**: Z jednostkami (million, thousand)
- **Daty**: Format YYYY lub pełne daty

## Rozwiązywanie Problemów

### Spider nie znajduje danych

**Rozwiązanie:**
1. Sprawdź czy strona jest dostępna: `curl -I [URL]`
2. Sprawdź czy robots.txt pozwala: `curl [URL]/robots.txt`
3. Zwiększ `DOWNLOAD_DELAY` do 3-5 sekund
4. Dodaj więcej źródeł do `start_urls`

### Dane są niepełne

**Rozwiązanie:**
1. Dodaj więcej wzorców w metodach `extract_*()`
2. Sprawdź logi: `grep "Finalized" logs/scrapy.log`
3. Uzupełnij ręcznie w `finalize_data()`

### Błąd: "403 Forbidden"

**Rozwiązanie:**
```python
custom_settings = {
    'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    'DOWNLOAD_DELAY': 3,
}
```

### Timeout

**Rozwiązanie:**
```python
custom_settings = {
    'DOWNLOAD_TIMEOUT': 30,  # zwiększ timeout
    'RETRY_TIMES': 3,
}
```

## Przykłady Użycia

### 1. Aktualizacja Danych Niemiec

```bash
# Scrape nowych danych
python3 scrape_country_data.py germany

# Porównaj z istniejącymi
diff resources/germany.json resources/germany.json.backup
```

### 2. Dodanie Nowego Kraju

```bash
# 1. Stwórz spider
cp src/country_scrapper/spiders/germany_spider.py \
   src/country_scrapper/spiders/poland_spider.py

# 2. Edytuj poland_spider.py (nazwa, URLe, domyślne wartości)

# 3. Dodaj do scrape_country_data.py:
countries = ['germany', 'france', 'poland']

# 4. Uruchom
python3 scrape_country_data.py poland
```

### 3. Scraping w Tle

```bash
# Uruchom w tle z logiem
nohup python3 scrape_country_data.py --all > scraper.log 2>&1 &

# Sprawdź postęp
tail -f scraper.log
```

## Zaawansowane

### Dodanie NLP do Ekstrakcji

```python
import spacy

nlp = spacy.load("en_core_web_sm")

def extract_with_nlp(self, text: str):
    doc = nlp(text)
    
    # Ekstrakcja encji
    for ent in doc.ents:
        if ent.label_ == "GPE":  # Geo-political entity
            self.country_data["_raw_data"]["bilateral_countries"].add(ent.text)
        elif ent.label_ == "MONEY":
            # Ekstrakcja PKB, budżetu, etc.
            pass
```

### Scraping z JavaScript

Dla stron wymagających JavaScript:

```bash
pip install scrapy-playwright
```

```python
class ModernSpider(scrapy.Spider):
    custom_settings = {
        'DOWNLOAD_HANDLERS': {
            'https': 'scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler',
        },
    }
```

## Maintanance

### Aktualizacja Danych

Zalecane: co 3-6 miesięcy
```bash
python3 scrape_country_data.py --all
```

### Monitoring Źródeł

Sprawdź czy URLe są aktualne:
```bash
# Test wszystkich URLi
for url in $(grep -o 'https://[^"]*' src/country_scrapper/spiders/germany_spider.py); do
    curl -I "$url" | head -1
done
```

## Etyka i Legalność

✅ **Dozwolone:**
- Scraping publicznych danych rządowych
- Przestrzeganie robots.txt
- Rozsądne opóźnienia między requestami
- Podanie User-Agent identyfikującego cel

❌ **Zabronione:**
- Łamanie CAPTCHA
- Ignorowanie robots.txt
- DDoS (zbyt częste requesty)
- Scraping danych osobowych

## Referencje

- [Scrapy Documentation](https://docs.scrapy.org/)
- [BeautifulSoup Docs](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [robots.txt Specification](https://www.robotstxt.org/)
