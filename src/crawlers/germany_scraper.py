#!/usr/bin/env python3
"""
Germany Data Scraper
Collects latest data about Germany from public sources
"""
import requests
from bs4 import BeautifulSoup
import json
import logging
from datetime import datetime
from typing import Dict, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GermanyScraper:
    """Scraper for collecting Germany data from various sources"""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
        )
        self.data = {
            "country_name": "Germany",
            "last_updated": datetime.now().isoformat(),
            "sources": [],
        }

    def scrape_wikipedia_basic_info(self) -> Dict:
        """Scrape basic information from Wikipedia"""
        url = "https://en.wikipedia.org/wiki/Germany"
        logger.info(f"Scraping Wikipedia: {url}")

        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "html.parser")

            # Get infobox data
            infobox = soup.find("table", {"class": "infobox"})
            if not infobox:
                logger.warning("Could not find infobox on Wikipedia")
                return {}

            data = {}

            # Extract population
            for row in infobox.find_all("tr"):
                header = row.find("th")
                if header and "Population" in header.get_text():
                    value = row.find("td")
                    if value:
                        # Try to find the population number
                        pop_text = value.get_text().strip()
                        # Extract first number that looks like population
                        import re

                        numbers = re.findall(r"[\d,]+", pop_text)
                        if numbers:
                            data["population"] = numbers[0].replace(",", "")

            # Extract capital
            for row in infobox.find_all("tr"):
                header = row.find("th")
                if header and "Capital" in header.get_text():
                    value = row.find("td")
                    if value:
                        data["capital"] = value.get_text().strip()

            # Extract GDP
            for row in infobox.find_all("tr"):
                header = row.find("th")
                if header and "GDP" in header.get_text():
                    value = row.find("td")
                    if value:
                        gdp_text = value.get_text().strip()
                        data["gdp_info"] = gdp_text[:200]  # First 200 chars

            self.data["sources"].append(
                {
                    "name": "Wikipedia",
                    "url": url,
                    "scraped_at": datetime.now().isoformat(),
                }
            )

            logger.info(f"Successfully scraped Wikipedia: {len(data)} fields")
            return data

        except Exception as e:
            logger.error(f"Error scraping Wikipedia: {e}")
            return {}

    def scrape_worldbank_data(self) -> Dict:
        """Scrape economic data from World Bank API"""
        # World Bank API for Germany (country code: DEU)
        url = "https://api.worldbank.org/v2/country/DEU/indicator/NY.GDP.MKTP.CD?format=json&per_page=1&date=2023:2023"
        logger.info(f"Fetching World Bank API: {url}")

        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            data_json = response.json()

            if len(data_json) > 1 and data_json[1]:
                gdp_data = data_json[1][0]

                self.data["sources"].append(
                    {
                        "name": "World Bank API",
                        "url": url,
                        "scraped_at": datetime.now().isoformat(),
                    }
                )

                logger.info("Successfully fetched World Bank data")
                return {
                    "gdp_current_usd": gdp_data.get("value"),
                    "gdp_year": gdp_data.get("date"),
                }

            return {}

        except Exception as e:
            logger.error(f"Error fetching World Bank data: {e}")
            return {}

    def scrape_cia_factbook(self) -> Dict:
        """Scrape data from CIA World Factbook"""
        url = "https://www.cia.gov/the-world-factbook/countries/germany/"
        logger.info(f"Scraping CIA Factbook: {url}")

        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "html.parser")

            data = {}

            # Look for military information
            military_section = soup.find("h2", string="Military and Security")
            if military_section:
                # Navigate to find military expenditure
                content = military_section.find_next("div")
                if content:
                    text = content.get_text()
                    if "military expenditure" in text.lower():
                        data["military_info"] = text[:500]

            self.data["sources"].append(
                {
                    "name": "CIA World Factbook",
                    "url": url,
                    "scraped_at": datetime.now().isoformat(),
                }
            )

            logger.info(f"Successfully scraped CIA Factbook: {len(data)} fields")
            return data

        except Exception as e:
            logger.error(f"Error scraping CIA Factbook: {e}")
            return {}

    def get_static_data(self) -> Dict:
        """Get static/known data about Germany"""
        return {
            "country_name": "Germany",
            "geographical_features": "Central Europe, bordered by Denmark, Poland, Czech Republic, Austria, Switzerland, France, Luxembourg, Belgium, Netherlands",
            "population": "84,000,000",  # Approximate 2024 data
            "climate": "Temperate and marine; cool, cloudy, wet winters and summers",
            "currency": "Euro (EUR)",
            "army_size": "183,000",  # Bundeswehr active personnel (2024)
            "key_bilateral_relations": [
                "France",
                "United States",
                "United Kingdom",
                "Poland",
                "Netherlands",
                "Italy",
                "China",
            ],
            "economic_strengths": "Automotive industry, mechanical engineering, chemical industry, renewable energy, precision instruments",
            "digitalization_level": "High - strong industry 4.0 adoption, leading in industrial automation",
            "political_economic_threats": "Energy dependency, aging population, competition from Asia in automotive sector, economic slowdown in EU",
            "military_threats": "Regional instability in Eastern Europe, cyber threats, terrorism",
            "development_milestones": "EU leadership, energy transition (Energiewende), Industry 4.0, digital transformation",
        }

    def scrape_all(self) -> Dict:
        """Run all scrapers and combine data"""
        logger.info("=" * 80)
        logger.info("Starting Germany data collection")
        logger.info("=" * 80)

        # Start with static data
        combined_data = self.get_static_data()

        # Scrape Wikipedia
        wiki_data = self.scrape_wikipedia_basic_info()
        combined_data.update(wiki_data)

        # Scrape World Bank
        wb_data = self.scrape_worldbank_data()
        combined_data.update(wb_data)

        # Scrape CIA Factbook (optional, may be slow)
        # cia_data = self.scrape_cia_factbook()
        # combined_data.update(cia_data)

        # Add metadata
        combined_data["last_updated"] = datetime.now().isoformat()
        combined_data["sources"] = self.data["sources"]

        logger.info("=" * 80)
        logger.info(f"Data collection complete: {len(combined_data)} fields")
        logger.info("=" * 80)

        return combined_data

    def save_to_json(self, data: Dict, filepath: str = "resources/germany_new.json"):
        """Save collected data to JSON file"""
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            logger.info(f"Data saved to {filepath}")
        except Exception as e:
            logger.error(f"Error saving data: {e}")


def main():
    """Main function to run the scraper"""
    scraper = GermanyScraper()

    # Collect all data
    data = scraper.scrape_all()

    # Print summary
    print("\n" + "=" * 80)
    print("COLLECTED DATA SUMMARY")
    print("=" * 80)
    for key, value in data.items():
        if key == "sources":
            print(f"\n{key}:")
            for source in value:
                print(f"  - {source['name']}: {source['url']}")
        elif isinstance(value, (list, dict)):
            print(f"{key}: {type(value).__name__} with {len(value)} items")
        else:
            value_str = str(value)
            if len(value_str) > 100:
                value_str = value_str[:100] + "..."
            print(f"{key}: {value_str}")

    # Save to file
    scraper.save_to_json(data)

    print("\n" + "=" * 80)
    print("✅ Scraping complete! Check resources/germany_new.json")
    print("=" * 80)


if __name__ == "__main__":
    main()
