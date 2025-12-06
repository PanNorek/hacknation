import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from pydantic_ai import Agent
from pydantic_ai.models.google import GoogleModel, GoogleModelSettings
from pydantic_ai.providers.google import GoogleProvider
from typing import List
from src.configuration import Configuration

load_dotenv()

# Load configuration
config = Configuration()

API_KEY = config.gemini_api_key or os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    raise ValueError(
        "GOOGLE_API_KEY environment variable is not set. "
        "Please create a .env file with GOOGLE_API_KEY=your_api_key"
    )

class HistoricalCorrelation(BaseModel):
    """Identified correlation between historical facts"""
    fact_1: str = Field(description="First historical fact or trend")
    fact_2: str = Field(description="Second historical fact or trend")
    correlation_description: str = Field(description="Description of how these facts are correlated")
    relevance_to_forecast: str = Field(description="Why this correlation matters for the forecast")

class NonObviousFactor(BaseModel):
    """Non-obvious factor that could influence outcomes"""
    factor_name: str = Field(description="Name of the non-obvious factor")
    description: str = Field(description="Description of the factor and why it's non-obvious")
    potential_impact: str = Field(description="How this factor could influence the outcome")

class ChainOfThoughtStep(BaseModel):
    """Single step in the chain of thought reasoning"""
    step_number: int = Field(description="Sequential step number")
    description: str = Field(description="What happens at this step")
    reasoning: str = Field(description="Why this step follows from the previous one")

class ForecastScenario(BaseModel):
    timeframe: str = Field(description="12-month or 36-month forecast")
    
    # Chain of Thought - krok po kroku
    historical_facts: List[str] = Field(description="Lista kluczowych faktów historycznych i obecnych trendów wykorzystanych w analizie")
    identified_correlations: List[HistoricalCorrelation] = Field(description="Zidentyfikowane korelacje między faktami historycznymi")
    non_obvious_factors: List[NonObviousFactor] = Field(description="Nieoczywiste czynniki zmian (czarne łabędzie, ukryte zależności)")
    chain_of_thought: List[ChainOfThoughtStep] = Field(description="Szczegółowy łańcuch rozumowania od faktów historycznych do prognozy")
    
    # Prognozy
    positive_forecast_1: str = Field(description="First positive scenario forecast")
    positive_forecast_2: str = Field(description="Second positive scenario forecast")
    negative_forecast_1: str = Field(description="First negative scenario forecast")
    negative_forecast_2: str = Field(description="Second negative scenario forecast")
    
    # Wyjaśnienia
    confidence: float = Field(ge=0.0, le=1.0, description="Confidence level of the forecast")
    confidence_explanation: str = Field(description="Detailed explanation of why this confidence level was assigned, including key uncertainties and known factors")
    reasoning: str = Field(description="Detailed reasoning for the forecasts")
    causality: str = Field(description="Clear causal chain explanation: how the global scenario leads to these specific outcomes for this country, including intermediate steps and dependencies")

class ForecastOutput(BaseModel):
    forecast_12_months: ForecastScenario
    forecast_36_months: ForecastScenario

# Configure provider with settings from configuration
provider = GoogleProvider(api_key=API_KEY)

settings = GoogleModelSettings(
    temperature=config.gemini_temperature,  # From config (default: 0.2)
    max_tokens=config.gemini_max_tokens,    # From config (default: 4096)
)

model = GoogleModel(config.gemini_model_name, provider=provider, settings=settings)

SYSTEM_PROMPT = """
**WAŻNE: Wszystkie odpowiedzi MUSZĄ być w języku polskim!**

**Rola i Cel:**
Jesteś zaawansowanym agentem sztucznej inteligencji, pełniącym funkcję Głównego Analityka Geopolitycznego. 
Twoim celem jest dostarczanie szczegółowych, wyjaśnialnych analiz geopolitycznych i tworzenie prawdopodobnych 
scenariuszy przyszłych wydarzeń w kontekście międzynarodowym.

**Zadanie:**
Na podstawie dostarczonego scenariusza globalnego oraz informacji o krajach, musisz wygenerować prognozy 
dla konkretnego kraju na dwa horyzonty czasowe: 12 miesięcy i 36 miesięcy.

**WSZYSTKIE ODPOWIEDZI MUSZĄ BYĆ PO POLSKU!**

Dla każdego horyzontu czasowego musisz przedstawić:
- 2 pozytywne scenariusze (szanse, możliwości)
- 2 negatywne scenariusze (zagrożenia, ryzyka)

**Wymagania:**
1. Każda prognoza musi być konkretna i realistyczna
2. Musisz uwzględnić specyfikę danego kraju (jego gospodarkę, relacje międzynarodowe, zasoby)
3. Prognozy muszą być spójne ze scenariuszem globalnym
4. **KLUCZOWE: Użyj szczegółowego, wyjaśnialnego toku myślenia (Chain of Thought)**
5. Każda prognoza powinna być wyjaśniona w kontekście dostępnych danych

**WYJAŚNIALNOŚĆ - Chain of Thought (NAJWAŻNIEJSZE):**

Dla każdej prognozy MUSISZ przedstawić:

1. **Fakty historyczne i obecne trendy:**
   - Wydobądź konkretne fakty historyczne z danych kraju
   - Zidentyfikuj obecne trendy globalne i lokalne
   - Lista 3-5 kluczowych faktów, które wykorzystasz w analizie
   - **UWZGLĘDNIJ WSZYSTKIE 6 CZYNNIKÓW SCENARIUSZA**, ale z wagami: najważniejsze to a) (30) i f) (25)

2. **Identyfikacja korelacji:**
   - Znajdź korelacje między faktami historycznymi A korelacje MIĘDZY CZYNNIKAMI SCENARIUSZA
   - Przykłady interakcji:
     * Czynnik a) (GPU↓) + Czynnik c) (PKB↓) = podwójne ograniczenie cyfryzacji
     * Czynnik b) (automotive↓) + Czynnik f) (tania ropa) = dylematy strategiczne przemysłu
     * Czynnik d) (Ukraina) + Czynnik e) (inwestycje) = wpływ na bezpieczeństwo dostaw
   - Wyjaśnij DLACZEGO te czynniki się wzmacniają lub osłabiają
   - Wyjaśnij jak ta SYNERGIA jest ISTOTNA dla bieżącej prognozy

3. **Nieoczywiste czynniki (Deep Research):**
   - Zidentyfikuj 2-3 nieoczywiste czynniki wynikające z KOMBINACJI czynników scenariusza
   - "Czarne łabędzie" związane z wieloczynnikowym scenariuszem
   - Ukryte zależności między 6 czynnikami (np. "Tania ropa (f) może paradoksalnie SPOWOLNIĆ transformację OZE w automotive (b)")
   - Efekty drugiego rzędu: "Czynnik A wpływa na B, co z kolei wpływa na C"
   - Wyjaśnij DLACZEGO te czynniki są nieoczywiste

4. **Łańcuch rozumowania (krok po kroku) - UWZGLĘDNIAJĄCY WAGI:**
   - Minimum 5-7 kroków
   - Każdy krok: "Jeżeli A (czynnik scenariusza), to B (konsekwencja), ponieważ C (mechanizm)"
   - **ROZPOCZNIJ od najważniejszych czynników (a=30, f=25)**
   - Następnie pokaż jak nakładają się inne czynniki (b=15, c=15, d=10, e=5)
   - Przykład:
     * Krok 1: [a, waga 30] Producent GPU traci 60% mocy → globalne niedobory GPU
     * Krok 2: [a] Globalne niedobory → wzrost cen GPU o 150-200% → opóźnienia w AI
     * Krok 3: [c, waga 15] Jednocześnie PKB strefy euro↓ 1.5% → mniej środków na inwestycje
     * Krok 4: [a+c] GPU drogie + mniej środków = podwójne ograniczenie dla ambicji AI kraju {country_name}
     * Krok 5: [f, waga 25] Równolegle: spadek cen ropy do 30-35 USD → presja na budżet Rosji
     * Krok 6: [d+f] Słaby rozejm + słaba Rosja ekonomicznie → możliwe zmiany geopolityczne
     * Krok 7: Kumulatywny wpływ wszystkich 6 czynników na {country_name} → scenariusze

**Format Odpowiedzi:**
Dla każdego horyzontu czasowego (12 i 36 miesięcy):

**NAJPIERW - CHAIN OF THOUGHT (WYJAŚNIALNOŚĆ):**
- Fakty historyczne: [lista 3-5 kluczowych faktów wykorzystanych w analizie]
- Zidentyfikowane korelacje: [2-3 korelacje między faktami, z wyjaśnieniem istotności]
- Nieoczywiste czynniki: [2-3 nieoczywiste czynniki, "czarne łabędzie", ukryte zależności]
- Łańcuch rozumowania: [4-6 kroków, każdy krok z jasnym przejściem: "Jeżeli A, to B, ponieważ C"]

**NASTĘPNIE - PROGNOZY:**
- Pozytywny scenariusz 1: [szczegółowy opis, powiązany z chain of thought]
- Pozytywny scenariusz 2: [szczegółowy opis, powiązany z chain of thought]
- Negatywny scenariusz 1: [szczegółowy opis, powiązany z chain of thought]
- Negatywny scenariusz 2: [szczegółowy opis, powiązany z chain of thought]

**WYJAŚNIENIA:**
- Pewność prognozy: [0.0-1.0]
- Wyjaśnienie pewności: [dlaczego taki poziom pewności? jakie są główne niepewności? jakie czynniki są znane i pewne?]
- Uzasadnienie: [szczegółowe wyjaśnienie logiki]
- Przyczynowość: [jasny łańcuch przyczynowo-skutkowy: Scenariusz globalny → Etap pośredni 1 → Etap pośredni 2 → Konkretny wpływ na kraj. Wyjaśnij mechanizmy i zależności.]

**Wymagania dotyczące przyczynowości:**
Musisz przedstawić jasny łańcuch przyczynowo-skutkowy, np.:
1. Scenariusz globalny: Producent GPU traci 60% mocy produkcyjnych
2. Bezpośredni efekt: Globalne niedobory GPU i wzrost cen o 150-200%
3. Efekt pośredni: Opóźnienia w projektach AI i data centers na całym świecie
4. Wpływ na kraj: [konkretny kraj] ma ambicje AI → opóźnienia w realizacji infrastruktury AI → skutki gospodarcze/polityczne

**Wymagania dotyczące pewności:**
Wyjaśnij poziom pewności uwzględniając:
- Jakie dane są pewne (fakty historyczne, obecne zdolności produkcyjne)
- Jakie są główne niepewności (zachowanie innych graczy, tempo odbudowy, reakcje rynku)
- Jakie założenia wpływają na prognozę
- Dlaczego pewność dla 36 miesięcy może różnić się od 12 miesięcy

Bądź zwięzły, ale kompletny. Każdy scenariusz powinien mieć 2-4 zdania.
"""

forecasting_agent = Agent(
    output_type=ForecastOutput,
    model=model,
    system_prompt=SYSTEM_PROMPT,
)


async def generate_forecast(
    country_name: str,
    country_resources: dict,
    other_countries: List[dict],
    scenario: str,
    scenario_weight: int
) -> ForecastOutput:
    """
    Generate a geopolitical forecast for a country based on a global scenario.
    
    Args:
        country_name: Name of the country to forecast for
        country_resources: Dictionary with country's resources and characteristics
        other_countries: List of dictionaries with other countries' resources
        scenario: The global scenario description
        scenario_weight: Importance weight of the scenario (0-100)
    
    Returns:
        ForecastOutput with 12-month and 36-month forecasts
    """
    
    # Build context about other countries
    max_countries = config.max_other_countries_context  # From config (default: 5)
    other_countries_context = "\n\n".join([
        f"**{country['country_name']}:**\n"
        f"- Populacja: {country['population']}\n"
        f"- Siły zbrojne: {country['army_size']}\n"
        f"- Mocne strony gospodarcze: {country['economic_strengths']}\n"
        f"- Kluczowe relacje bilateralne: {', '.join(country['key_bilateral_relations'])}"
        for country in other_countries[:max_countries]  # Limit from config to avoid token limits
    ])
    
    prompt = f"""
**Kraj do analizy: {country_name}**

**Charakterystyka kraju:**
- Cechy geograficzne: {country_resources['geographical_features']}
- Populacja: {country_resources['population']}
- Klimat: {country_resources['climate']}
- Mocne strony gospodarcze: {country_resources['economic_strengths']}
- Wielkość armii: {country_resources['army_size']}
- Poziom cyfryzacji: {country_resources['digitalization_level']}
- Waluta: {country_resources['currency']}
- Kluczowe relacje bilateralne: {', '.join(country_resources['key_bilateral_relations'])}
- Zagrożenia polityczne/gospodarcze: {country_resources['political_economic_threats']}
- Zagrożenia militarne: {country_resources['military_threats']}
- Kamienie milowe rozwoju: {country_resources['development_milestones']}

**Scenariusz globalny - KOMPLEKSOWY (łączna waga: {scenario_weight}/100):**
{scenario}

**WAŻNE: To jest JEDEN złożony scenariusz globalny składający się z 6 współzależnych czynników.**
Musisz analizować ich wzajemne oddziaływanie i kumulatywny wpływ na kraj {country_name}.

**Wagi poszczególnych czynników:**
- a) Katastrofa GPU - waga 30/100 (najsilniejszy pojedynczy czynnik)
- b) Kryzys automotive w Europie - waga 15/100
- c) Spadek PKB strefy euro - waga 15/100
- d) Rozejm na Ukrainie - waga 10/100
- e) Inwestycje w Ukrainie - waga 5/100
- f) Rewolucja energetyczna i spadek cen ropy - waga 25/100 (drugi najsilniejszy czynnik)

**Kontekst międzynarodowy - inne kluczowe kraje:**
{other_countries_context}

**Zadanie:**
Wygeneruj szczegółowe prognozy dla kraju {country_name} na 12 i 36 miesięcy, uwzględniając:
1. Wpływ CAŁEGO scenariusza globalnego (wszystkie 6 czynników razem) na ten konkretny kraj
2. Interakcje między czynnikami (np. spadek PKB + kryzys automotive = podwójna presja na przemysł)
3. Wagi istotności - silniejsze czynniki (a=30, f=25) powinny mieć większy wpływ w analizie
4. Jego specyficzne mocne strony i słabości w kontekście WSZYSTKICH 6 czynników
5. Relacje z innymi krajami wymienionymi w kontekście
6. Bieżące zagrożenia i możliwości wynikające z KOMBINACJI czynników

Dla każdego horyzontu czasowego przedstaw 2 pozytywne i 2 negatywne scenariusze.

**KLUCZOWE: Analizuj synergię i interakcje między czynnikami:**
- Jak czynnik a) (GPU) wzmacnia lub osłabia wpływ czynnika c) (PKB↓)?
- Jak czynnik f) (tania ropa) wpływa na czynnik b) (kryzys automotive)?
- Jak czynniki d) i e) (Ukraina) łączą się z bezpieczeństwem energetycznym?
- Które kombinacje czynników są najbardziej korzystne/niekorzystne dla {country_name}?

**PRZYKŁAD CHAIN OF THOUGHT - KOMPLEKSOWY, WIELOCZYNNIKOWY (Wzór do naśladowania):**

Fakty historyczne:
1. "W latach 2020-2021 niedobory półprzewodników spowolniły przemysł motoryzacyjny o 15%" [powiązane z czynnikiem a]
2. "{country_name} posiada rozwiniętą branżę ICT z ambicjami w AI" [podatność na czynnik a]
3. "{country_name} ma silny sektor automotive powiązany z Niemcami i Francją" [podatność na czynnik b]
4. "Historyczne kryzysy energetyczne (1973, 2022) doprowadziły do transformacji energetycznej" [powiązane z czynnikiem f]
5. "Relacje z Ukrainą są kluczowe dla bezpieczeństwa regionalnego" [powiązane z czynnikami d, e]

Korelacje (MIĘDZY CZYNNIKAMI SCENARIUSZA):
1. Korelacja a+c: "Niedobory GPU (a, waga 30)" ↔ "Spadek PKB (c, waga 15)"
   - GPU drogie + mniej środków w budżecie = podwójne ograniczenie cyfryzacji
   - Istotność: Razem waga 45/100 - to prawie połowa wpływu scenariusza!

2. Korelacja b+f: "Kryzys automotive (b, waga 15)" ↔ "Tania ropa (f, waga 25)"
   - Paradoks: tania ropa może SPOWOLNIĆ transformację na elektryki (mniej motywacji)
   - ALE: konkurencja z Azji wymusza transformację mimo taniej ropy
   - Istotność: Razem waga 40/100 - kluczowa dla przemysłu ciężkiego

3. Korelacja d+e+f: "Ukraina (d+e, waga 15)" ↔ "Słaba Rosja przez tanią ropę (f, waga 25)"
   - Słabsza Rosja ekonomicznie może oznaczać stabilniejszy rozejm
   - ALE: może też próbować destabilizacji jako desperacki ruch

Nieoczywiste czynniki (z KOMBINACJI czynników):
1. "Efekt kaskadowy a→b→c": GPU↓ spowalnia automotive tech → kryzys automotive pogłębia się → PKB spada jeszcze bardziej
   - Opis: Trzy czynniki tworzą spiralę spowolnienia gospodarczego
   - Wpływ: {country_name} z silnym automotive może być szczególnie dotknięty

2. "Paradoks taniej ropy (f)": Tania ropa POWINNA pomóc gospodarce, ALE:
   - Spowalnia transformację OZE (mniej pilności)
   - Osłabia Rosję → niestabilność geopolityczna (d)
   - Uderza w kraje naftowe, które są partnerami handlowymi
   - Opis: Pozornie pozytywny czynnik ma ukryte negatywne konsekwencje

3. "Okno możliwości z Ukrainy (d+e)": Podczas gdy Rosja słabnie, inwestycje w Ukrainie rosną
   - {country_name} może wzmocnić relacje z Ukrainą i dostęp do surowców krytycznych
   - Nieoczywiste: To może być kluczowa szansa geopolityczna

Łańcuch rozumowania (UWZGLĘDNIAJĄCY WAGI I INTERAKCJE):

Krok 1 [a, waga 30 - NAJWAŻNIEJSZY]: Katastrofa naturalna → Producent GPU traci 60% mocy
→ Uzasadnienie: Fizyczne zniszczenie fabryk = natychmiastowy spadek produkcji
→ Globalne niedobory GPU, ceny rosną o 150-200%

Krok 2 [a→wpływ na {country_name}]: {country_name} ma ambicje AI (big data centers, AI giga factories)
→ Uzasadnienie: GPU są kluczowe dla AI, niedobory blokują realizację planów
→ Opóźnienia w projektach AI o 12-24 miesiące

Krok 3 [c, waga 15]: Jednocześnie PKB strefy euro spada o 1.5%
→ Uzasadnienie: Recesja w UE = mniej środków w budżetach krajowych
→ {country_name} ma mniej pieniędzy na inwestycje w AI

Krok 4 [a+c, SYNERGIA waga 45]: GPU drogie + mniej budżetu = podwójny problem
→ Uzasadnienie: Dwa czynniki się WZMACNIAJĄ - nie tylko drogie GPU, ale i brak środków
→ Ambicje AI {country_name} są poważnie zagrożone

Krok 5 [b, waga 15]: Przemysł automotive w Europie w kryzysie (zyski tylko 30% normy)
→ Uzasadnienie: Konkurencja z Azji + wolna transformacja na elektryki
→ {country_name} ma silny sektor automotive → bezpośredni wpływ na PKB i zatrudnienie

Krok 6 [f, waga 25 - DRUGI NAJWAŻNIEJSZY]: Równolegle ropa spada do 30-35 USD/baryłka
→ Uzasadnienie: Nowe złoża w Ameryce Południowej + wzrost OZE = nadpodaż
→ Presja na budżet Rosji (ropa to 40% dochodów budżetowych)

Krok 7 [d+f, INTERAKCJA]: Słaby rozejm na Ukrainie + słaba Rosja ekonomicznie
→ Uzasadnienie: Rosja pod presją ekonomiczną ma mniej środków na eskalację
→ Potencjalnie stabilniejsza sytuacja w regionie (szansa dla {country_name})

Krok 8 [e]: Inwestycje USA w surowce krytyczne na Ukrainie
→ Uzasadnienie: USA zabezpiecza łańcuchy dostaw, konkurencja o wpływy
→ {country_name} może wzmocnić relacje z Ukrainą (e) i dostęp do surowców

Krok 9 [KUMULATYWNY WPŁYW wszystkich 6 czynników]:
→ Negatywne: a+b+c = technologiczne i gospodarcze spowolnienie (waga 60/100)
→ Pozytywne: f+d+e = szanse geopolityczne i energetyczne (waga 40/100)
→ Ostateczny balans zależy od specyfiki {country_name} → scenariusze

**PAMIĘTAJ: Odpowiedź MUSI być w języku polskim! Wszystkie scenariusze, wyjaśnienia, uzasadnienia i analiza przyczynowości muszą być po polsku!**

**KLUCZOWE: Wyjaśnialność jest NAJWAŻNIEJSZA! Pracownik MSZ musi zrozumieć DLACZEGO doszedłeś do danej prognozy. Każdy krok musi być logiczny i oparty na faktach.**
"""
    
    try:
        result = await forecasting_agent.run(prompt)
        return result.output
    except Exception as e:
        raise Exception(f"Error generating forecast: {str(e)}")
