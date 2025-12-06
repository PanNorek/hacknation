# Jak Uruchamiać GitHub Actions On-Demand

## 🎯 Przegląd

Masz dwa workflows do aktualizacji danych krajów:

1. **Update Germany Data** - Automatyczny i ręczny update dla Niemiec
2. **Update All Countries Data** - Ręczny update dla wielu krajów naraz

## 🚀 Metoda 1: Przez GitHub Web UI

### Krok 1: Przejdź do Actions

1. Otwórz repozytorium na GitHub
2. Kliknij zakładkę **"Actions"** u góry

### Krok 2: Wybierz Workflow

Zobaczysz dwa workflows:

- **Update Germany Data** ⚡ (codzienne auto + manual)
- **Update All Countries Data** 🌍 (tylko manual)

### Krok 3: Uruchom Workflow

#### Dla pojedynczego kraju (Niemcy):

1. Kliknij **"Update Germany Data"**
2. Kliknij przycisk **"Run workflow"** (po prawej stronie)
3. Wybierz opcje:
   - **Branch**: `main` (lub inny)
   - **Force update**: `false` (normalnie) lub `true` (pełna aktualizacja)
   - **Commit message**: opcjonalnie własna wiadomość
   - **Delay between requests**: `2` (sekundy między requestami)
4. Kliknij zielony przycisk **"Run workflow"**

#### Dla wielu krajów:

1. Kliknij **"Update All Countries Data"**
2. Kliknij przycisk **"Run workflow"**
3. Wypełnij:
   - **Countries**: `germany` lub `germany,france,poland` lub `all`
   - **Force update**: `false` lub `true`
4. Kliknij **"Run workflow"**

### Krok 4: Monitoruj Postęp

- Workflow pojawi się na liście
- Kliknij aby zobaczyć live logs
- Poczekaj aż status zmieni się na ✅ zielony

---

## 🖥️ Metoda 2: Przez GitHub CLI (gh)

### Instalacja GitHub CLI

```bash
# Ubuntu/Debian
sudo apt install gh

# macOS
brew install gh

# Logowanie
gh auth login
```

### Uruchomienie Workflow

#### Update Niemiec (domyślne parametry):

```bash
gh workflow run "Update Germany Data"
```

#### Update Niemiec z custom parametrami:

```bash
gh workflow run "Update Germany Data" \
  -f force_update=false \
  -f commit_message="Manual update: Testing new scraper" \
  -f delay_between_requests=3
```

#### Update wielu krajów:

```bash
gh workflow run "Update All Countries Data" \
  -f countries="germany,france" \
  -f force_update=false
```

#### Update wszystkich krajów:

```bash
gh workflow run "Update All Countries Data" \
  -f countries="all" \
  -f force_update=true
```

### Sprawdzenie statusu:

```bash
# Lista ostatnich runs
gh run list --workflow="Update Germany Data"

# Szczegóły konkretnego run
gh run view <run-id>

# Live logs
gh run watch <run-id>
```

---

## 🔧 Metoda 3: Przez API (curl/Python)

### Przygotowanie

1. Wygeneruj Personal Access Token:
   - GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
   - Scopes: `repo`, `workflow`
2. Zapisz token bezpiecznie

### Curl - Update Niemiec:

```bash
GITHUB_TOKEN="your_token_here"
REPO_OWNER="your_username"
REPO_NAME="hacknation"

curl -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer $GITHUB_TOKEN" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/$REPO_OWNER/$REPO_NAME/actions/workflows/update-germany-data.yml/dispatches \
  -d '{
    "ref": "main",
    "inputs": {
      "force_update": "false",
      "commit_message": "API triggered update",
      "delay_between_requests": "2"
    }
  }'
```

### Python script:

```python
import requests

GITHUB_TOKEN = "your_token_here"
REPO_OWNER = "your_username"
REPO_NAME = "hacknation"

def trigger_germany_update(force=False, message=None, delay=2):
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/actions/workflows/update-germany-data.yml/dispatches"

    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "X-GitHub-Api-Version": "2022-11-28"
    }

    data = {
        "ref": "main",
        "inputs": {
            "force_update": str(force).lower(),
            "commit_message": message or "API triggered update",
            "delay_between_requests": str(delay)
        }
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 204:
        print("✅ Workflow triggered successfully!")
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)

# Użycie
trigger_germany_update(force=False, message="Scheduled API update")
```

---

## 📊 Parametry Workflows

### Update Germany Data

| Parametr                 | Typ    | Domyślnie | Opis                                              |
| ------------------------ | ------ | --------- | ------------------------------------------------- |
| `force_update`           | choice | `false`   | Ignoruj istniejące dane, pobierz wszystko od nowa |
| `commit_message`         | string | auto      | Własna wiadomość commit                           |
| `delay_between_requests` | number | `2`       | Opóźnienie między requestami (sekundy)            |

### Update All Countries Data

| Parametr       | Typ    | Domyślnie | Opis                                    |
| -------------- | ------ | --------- | --------------------------------------- |
| `countries`    | string | `germany` | Kraje rozdzielone przecinkami lub `all` |
| `force_update` | choice | `false`   | Pełna aktualizacja wszystkich krajów    |

---

## 🔔 Powiadomienia

### Email notifications

GitHub automatycznie wysyła email gdy:

- Workflow się nie powiedzie
- Workflow zakończy się sukcesem (opcjonalnie w ustawieniach)

### Slack/Discord Webhook

Dodaj do workflow:

```yaml
- name: Notify Slack
  if: always()
  uses: 8398a7/action-slack@v3
  with:
    status: ${{ job.status }}
    webhook_url: ${{ secrets.SLACK_WEBHOOK }}
```

---

## 🐛 Troubleshooting

### "Workflow not found"

- Upewnij się że workflow file jest w `main` branch
- Sprawdź czy plik jest w `.github/workflows/`

### "Secret not found"

- Dodaj `GEMINI_API_KEY` w Settings → Secrets → Actions

### "No changes detected"

- To OK! Znaczy że dane są aktualne
- Użyj `force_update=true` aby wymusić update

### Workflow się zawiesza

- Sprawdź czy strony rządowe są dostępne
- Zwiększ `delay_between_requests`
- Sprawdź logi w Actions tab

---

## 📅 Harmonogramy

### Aktualne ustawienia:

- **Germany**: Codziennie o 3:00 UTC (automatycznie)

### Zmiana harmonogramu:

Edytuj `.github/workflows/update-germany-data.yml`:

```yaml
schedule:
  - cron: "0 3 * * *" # Codziennie o 3:00 UTC
  - cron: "0 */6 * * *" # Co 6 godzin
  - cron: "0 0 * * 0" # Co tydzień w niedzielę
```

---

## 🎯 Najlepsze Praktyki

1. **Nie uruchamiaj zbyt często**: Rate limiting API
2. **Monitoruj koszty**: Gemini API ma limity
3. **Sprawdzaj logi**: Actions → Run → View logs
4. **Backup przed force_update**: Na wypadek problemów
5. **Test na branch**: Najpierw test, potem main

---

## 💡 Przykłady Użycia

### Szybka aktualizacja przed spotkaniem:

```bash
gh workflow run "Update Germany Data" \
  -f commit_message="Pre-meeting data refresh"
```

### Pełna regeneracja wszystkich danych:

```bash
gh workflow run "Update All Countries Data" \
  -f countries="all" \
  -f force_update=true
```

### Wolniejsze scraping (gentle):

```bash
gh workflow run "Update Germany Data" \
  -f delay_between_requests=5
```

---

## 📚 Zobacz również

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [GitHub CLI Manual](https://cli.github.com/manual/)
- [SCRAPER_GUIDE.md](SCRAPER_GUIDE.md) - Przewodnik po scraperach
- [GITHUB_ACTIONS.md](GITHUB_ACTIONS.md) - Szczegóły techniczne
