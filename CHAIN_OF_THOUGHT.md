# Chain of Thought - Wyjaśnialność Analiz Geopolitycznych

## Przegląd

System został zaprojektowany z naciskiem na **wyjaśnialność** (explainability) generowanych analiz geopolitycznych. Z punktu widzenia pracownika MSZ kluczowe jest zrozumienie **jak** i **dlaczego** system doszedł do konkretnej prognozy.

## Komponenty Chain of Thought

### 1. Fakty Historyczne i Obecne Trendy

System identyfikuje i wykorzystuje konkretne fakty historyczne oraz obecne trendy, które mają znaczenie dla prognozy:

```
Przykład:
- "W latach 2020-2021 niedobory półprzewodników spowolniły przemysł motoryzacyjny o 15%"
- "Atlantis posiada rozwiniętą branżę ICT z ambicjami w AI (big data centers, AI giga factories)"
- "Historycznie, kryzysy w łańcuchach dostaw doprowadziły do dywersyfikacji dostawców"
```

**Cel:** Pokazanie, że prognozy są oparte na sprawdzalnych faktach, nie na spekulacji.

### 2. Zidentyfikowane Korelacje

System wykrywa korelacje między faktami historycznymi i wyjaśnia ich znaczenie:

```
Przykład:
Korelacja: "Niedobory chipów" ↔ "Spowolnienie sektora ICT"
- Fakt 1: W przeszłości (2020-2021) embargo na procesory
- Fakt 2: Opóźnienia projektów ICT o 6-18 miesięcy
- Opis korelacji: Niedobory chipów bezpośrednio spowalniają rozwój technologiczny
- Istotność: Atlantis ma ambicje AI, więc będzie bezpośrednio dotknięty
```

**Cel:** Pokazanie zależności między zjawiskami opartych na danych historycznych.

### 3. Nieoczywiste Czynniki (Deep Research)

System identyfikuje czynniki, które nie są oczywiste na pierwszy rzut oka:

```
Przykład:
1. "Ukryty efekt konkurencji":
   - Podczas gdy Atlantis czeka na GPU, Niemcy i Francja mogą przyspieszyć
     własne projekty AI wykorzystując alternatywne źródła

2. "Czarny łabędź - konsolidacja rynku":
   - Niedobory mogą doprowadzić do monopolizacji rynku GPU
```

**Cel:** Identyfikacja "czarnych łabędzi" i ukrytych zależności, które mogą zaskoczyć analityków.

### 4. Łańcuch Rozumowania (Krok po Kroku)

System przedstawia szczegółowy łańcuch logiczny od scenariusza globalnego do konkretnego wpływu:

```
Krok 1: Katastrofa naturalna → Producent GPU traci 60% mocy
→ Uzasadnienie: Fizyczne zniszczenie fabryk oznacza natychmiastowy spadek produkcji

Krok 2: Spadek produkcji o 60% → Globalne niedobory GPU i wzrost cen o 150-200%
→ Uzasadnienie: Popyt pozostaje stały, podaż spadła → prawo podaży i popytu

Krok 3: Wzrost cen GPU → Opóźnienia w projektach AI na całym świecie
→ Uzasadnienie: Projekty AI wymagają tysięcy GPU, wzrost cen czyni je nieopłacalnymi

Krok 4: Atlantis ma ambicje AI → Bezpośredni wpływ na plany infrastrukturalne
→ Uzasadnienie: Planowane inwestycje wymagają GPU, niedobory blokują realizację

Krok 5: Opóźnienia w realizacji → Ryzyko utraty przewagi wobec Niemiec i Francji
→ Uzasadnienie: Inne kraje mogą wykorzystać alternatywne źródła

Krok 6: Ostateczny wpływ → [konkretne scenariusze pozytywne i negatywne]
```

**Cel:** Pokazanie jasnej ścieżki logicznej od przyczyny do skutku.

## Struktura Wyjścia

Dla każdej prognozy (12 miesięcy i 36 miesięcy) system generuje:

### 📚 Fakty Historyczne

Lista 3-5 kluczowych faktów wykorzystanych w analizie

### 🔗 Zidentyfikowane Korelacje

2-3 korelacje między faktami z wyjaśnieniem istotności

### 🦢 Nieoczywiste Czynniki

2-3 nieoczywiste czynniki, "czarne łabędzie", ukryte zależności

### 🎯 Łańcuch Rozumowania

4-6 kroków z jasnym przejściem: "Jeżeli A, to B, ponieważ C"

### 📊 Prognozy

- 2 pozytywne scenariusze
- 2 negatywne scenariusze

### 💡 Wyjaśnienia

- Pewność prognozy (0.0-1.0)
- Wyjaśnienie poziomu pewności
- Szczegółowe uzasadnienie
- Łańcuch przyczynowo-skutkowy

## Przykład Użycia

```python
model = WorldModel()

# Definiowanie scenariusza globalnego (wielowątkowy)
model.scenario = {
    "description": """
    a) Katastrofa naturalna - producent GPU stracił 60% mocy (waga: 30)
    b) Kryzys przemysłu motoryzacyjnego w Europie (waga: 15)
    c) Spadek PKB strefy euro o 1.5% (waga: 15)
    d) Słaby rozejm na Ukrainie (waga: 10)
    e) Inwestycje USA/UE w Ukrainie (waga: 5)
    f) Wzrost OZE i spadek cen ropy do 30-35 USD/baryłka (waga: 25)
    """,
    "total_weight": 100
}

# Uruchomienie symulacji
# Krok 1: Eksploracja (agenci zbierają dane o innych krajach)
model.step()

# Krok 2: Prognozowanie (agenci generują szczegółowe prognozy z Chain of Thought)
model.step()
```

## Wartość dla Pracownika MSZ

1. **Transparentność:** Każda prognoza jest w pełni wyjaśniona
2. **Weryfikowalność:** Fakty historyczne można zweryfikować
3. **Zrozumiałość:** Jasny łańcuch logiczny od przyczyny do skutku
4. **Deep Research:** Identyfikacja nieoczywistych czynników i korelacji
5. **Porównywalność:** Można porównać prognozy dla różnych krajów

## Techniczne Szczegóły

- **Model AI:** Gemini 2.0 Flash
- **Temperatura:** 0.2 (niska temperatura dla spójności)
- **Język:** Polski (wszystkie analizy)
- **Format:** Strukturyzowane dane (Pydantic models)

## Ograniczenia

- System opiera się na danych dostarczonych w JSON dla każdego kraju
- Jakość prognoz zależy od jakości danych wejściowych
- Nieoczywiste czynniki są identyfikowane na podstawie wzorców w danych treningowych modelu AI
- Prognozy na 36 miesięcy mają naturalnie niższą pewność niż na 12 miesięcy
