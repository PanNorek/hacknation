# Crawlers / Scrapers

## Overview

This directory contains web scrapers for collecting country data from official government sources.

## Available Scrapers

### 1. **germany_advanced_scraper.py** ⭐ Recommended

Advanced scraper with LLM-powered data extraction and smart update logic.

**Features:**
- Multi-source scraping (7 official German government websites)
- Google Gemini LLM for intelligent data extraction
- **Smart data preservation** - only updates fields that were found
- Preserves existing data for fields with "NOT_FOUND" values
- Clean JSON output (no metadata)

**Usage:**
```bash
python3 src/crawlers/germany_advanced_scraper.py
```

**See:** [SCRAPER_UPDATE_LOGIC.md](/home/rafal/coding/hacknation/SCRAPER_UPDATE_LOGIC.md) for details on data preservation.

### 2. **germany_scraper.py**

Basic scraper using Wikipedia and World Bank API.

**Usage:**
```bash
python3 src/crawlers/germany_scraper.py
```

### 3. **country_scraper_template.py**

Template for creating scrapers for other countries.

## Key Features

### 🔄 Smart Data Preservation

Scrapers use intelligent merge logic:
- ✅ Updates only fields that were successfully found
- 💾 Preserves existing data when new scraping fails or returns "NOT_FOUND"
- 📝 Logs which fields were updated vs preserved

### 🤖 LLM-Powered Extraction

Uses Google Gemini to:
- Intelligently extract structured data from unstructured web content
- Understand context and synthesize information from multiple sources
- Return "NOT_FOUND" for missing data (enables preservation logic)

### 🧹 Clean Output

Final JSON files contain only structured country data:
- No sources metadata
- No timestamps
- No interim data
- Clean, ready-to-use format

## Output Format

All scrapers produce JSON in this format:

```json
{
  "country_name": "Germany",
  "geographical_features": "...",
  "population": "84,000,000",
  "climate": "...",
  "economic_strengths": "...",
  "army_size": "183,000",
  "digitalization_level": "...",
  "currency": "Euro (EUR)",
  "key_bilateral_relations": ["France", "Poland", ...],
  "political_economic_threats": "...",
  "military_threats": "...",
  "development_milestones": "..."
}
```

## Creating New Scrapers

### Option 1: Copy and Modify Template

```bash
cp src/crawlers/country_scraper_template.py src/crawlers/france_scraper.py
# Edit france_scraper.py: change URLs, country name, etc.
```

### Option 2: Extend Advanced Scraper

Modify `germany_advanced_scraper.py` for your country:
1. Change `start_urls` to target country's government websites
2. Update `country_name` in CountryData model
3. Adjust system prompt if needed

## Best Practices

### ✅ DO:
- Use official government sources
- Implement request delays (2-3 seconds)
- Respect robots.txt
- Log all actions
- Handle errors gracefully
- Preserve existing data when scraping fails

### ❌ DON'T:
- Scrape too frequently (DDoS risk)
- Ignore robots.txt
- Store unnecessary metadata in final output
- Overwrite good data with guesses

## Configuration

Scrapers use configuration from `/home/rafal/coding/hacknation/src/configuration.py`:

```python
GEMINI_API_KEY=your_key_here
GEMINI_MODEL_NAME=gemini-2.0-flash
GEMINI_TEMPERATURE=0.1  # Low for factual extraction
```

## Troubleshooting

### Scraper returns all "NOT_FOUND"

**Check:**
1. Are the source websites accessible?
2. Is the LLM API key valid?
3. Review raw scraped content in logs

### Data not updating

**Solution:**
- Check logs for which fields were "preserved"
- Verify LLM is finding information in scraped content
- Try scraping manually to verify source availability

### API rate limits

**Solution:**
- Increase delays between requests
- Reduce number of sources
- Use caching for repeated runs

## Documentation

- [SCRAPER_GUIDE.md](/home/rafal/coding/hacknation/SCRAPER_GUIDE.md) - Comprehensive guide
- [SCRAPER_UPDATE_LOGIC.md](/home/rafal/coding/hacknation/SCRAPER_UPDATE_LOGIC.md) - Data preservation logic
- [CONFIG.md](/home/rafal/coding/hacknation/CONFIG.md) - Configuration options

## Maintenance

### Updating Data

Recommended frequency: Every 3-6 months

```bash
# Update single country
python3 src/crawlers/germany_advanced_scraper.py

# Backup before major updates
cp resources/germany.json resources/germany_backup_$(date +%Y%m%d).json
```

### Monitoring Sources

Check if source URLs are still valid:

```bash
# Test Germany sources
curl -I https://www.auswaertiges-amt.de/en
curl -I https://www.bmvg.de/en
# etc.
```