#!/usr/bin/env python3
"""
Generic Country Data Scraper Template
Can be customized for any country
"""
import requests
from bs4 import BeautifulSoup
import json
import logging
from datetime import datetime
from typing import Dict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CountryScraper:
    """Generic scraper for collecting country data"""

    def __init__(self, country_name: str, country_code: str, wikipedia_url: str):
        """
        Initialize scraper

        Args:
            country_name: Full country name (e.g., "France")
            country_code: ISO 3-letter country code (e.g., "FRA")
            wikipedia_url: URL to country's Wikipedia page
        """
        self.country_name = country_name
        self.country_code = country_code
        self.wikipedia_url = wikipedia_url

        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
        )
        self.sources = []

    def scrape_wikipedia_basic_info(self) -> Dict:
        """Scrape basic information from Wikipedia"""
        logger.info(f"Scraping Wikipedia: {self.wikipedia_url}")

        try:
            response = self.session.get(self.wikipedia_url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "html.parser")

            infobox = soup.find("table", {"class": "infobox"})
            if not infobox:
                logger.warning("Could not find infobox")
                return {}

            data = {}

            # Extract population
            for row in infobox.find_all("tr"):
                header = row.find("th")
                if header and "Population" in header.get_text():
                    value = row.find("td")
                    if value:
                        import re

                        numbers = re.findall(r"[\d,]+", value.get_text())
                        if numbers:
                            data["population"] = numbers[0].replace(",", "")

            # Extract capital
            for row in infobox.find_all("tr"):
                header = row.find("th")
                if header and "Capital" in header.get_text():
                    value = row.find("td")
                    if value:
                        data["capital"] = value.get_text().strip().split("[")[0]

            self.sources.append(
                {
                    "name": "Wikipedia",
                    "url": self.wikipedia_url,
                    "scraped_at": datetime.now().isoformat(),
                }
            )

            logger.info(f"Successfully scraped Wikipedia: {len(data)} fields")
            return data

        except Exception as e:
            logger.error(f"Error scraping Wikipedia: {e}")
            return {}

    def scrape_worldbank_gdp(self) -> Dict:
        """Scrape GDP data from World Bank API"""
        url = f"https://api.worldbank.org/v2/country/{self.country_code}/indicator/NY.GDP.MKTP.CD?format=json&per_page=1&date=2023:2023"
        logger.info(f"Fetching World Bank API")

        try:
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            data_json = response.json()

            if len(data_json) > 1 and data_json[1]:
                gdp_data = data_json[1][0]

                self.sources.append(
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

    def get_template_data(self) -> Dict:
        """
        Get template data structure - MUST BE CUSTOMIZED FOR EACH COUNTRY

        Returns:
            Dictionary with country-specific data
        """
        return {
            "country_name": self.country_name,
            "geographical_features": "TODO: Add geographical features",
            "population": "TODO: Add population",
            "climate": "TODO: Add climate description",
            "currency": "TODO: Add currency",
            "army_size": "TODO: Add army size",
            "key_bilateral_relations": ["TODO: Add key partners"],
            "economic_strengths": "TODO: Add economic strengths",
            "digitalization_level": "TODO: Add digitalization level",
            "political_economic_threats": "TODO: Add political/economic threats",
            "military_threats": "TODO: Add military threats",
            "development_milestones": "TODO: Add development milestones",
        }

    def scrape_all(self) -> Dict:
        """Run all scrapers and combine data"""
        logger.info("=" * 80)
        logger.info(f"Starting data collection for {self.country_name}")
        logger.info("=" * 80)

        # Start with template
        combined_data = self.get_template_data()

        # Scrape Wikipedia
        wiki_data = self.scrape_wikipedia_basic_info()
        combined_data.update(wiki_data)

        # Scrape World Bank
        wb_data = self.scrape_worldbank_gdp()
        combined_data.update(wb_data)

        # Add metadata
        combined_data["last_updated"] = datetime.now().isoformat()
        combined_data["sources"] = self.sources

        logger.info("=" * 80)
        logger.info(f"Data collection complete: {len(combined_data)} fields")
        logger.info("=" * 80)

        return combined_data

    def save_to_json(self, data: Dict, filepath: str = None):
        """Save collected data to JSON file"""
        if filepath is None:
            filepath = (
                f"resources/{self.country_name.lower().replace(' ', '_')}_new.json"
            )

        try:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            logger.info(f"Data saved to {filepath}")
        except Exception as e:
            logger.error(f"Error saving data: {e}")


# Example usage for France
class FranceScraper(CountryScraper):
    """Scraper specifically for France"""

    def __init__(self):
        super().__init__(
            country_name="France",
            country_code="FRA",
            wikipedia_url="https://en.wikipedia.org/wiki/France",
        )

    def get_template_data(self) -> Dict:
        """France-specific data"""
        return {
            "country_name": "France",
            "geographical_features": "Western Europe, borders with Belgium, Luxembourg, Germany, Switzerland, Italy, Spain, Andorra, Monaco",
            "population": "68,000,000",
            "climate": "Generally cool winters and mild summers, but mild winters and hot summers along the Mediterranean",
            "currency": "Euro (EUR)",
            "army_size": "205,000",
            "key_bilateral_relations": [
                "Germany",
                "United Kingdom",
                "United States",
                "Italy",
                "Spain",
                "Belgium",
                "China",
            ],
            "economic_strengths": "Tourism, aerospace, luxury goods, wine, agriculture, nuclear energy, defense industry",
            "digitalization_level": "High - strong digital infrastructure, La French Tech initiative, growing tech sector",
            "political_economic_threats": "Public debt, pension system reform challenges, social unrest, competition in manufacturing",
            "military_threats": "Terrorism, cyber threats, regional instability in Sahel region",
            "development_milestones": "EU leadership, nuclear energy independence, high-speed rail network, aerospace industry leadership",
        }


def main():
    """Example: Scrape France data"""
    print("Country Scraper Template")
    print("=" * 80)
    print("\nAvailable country scrapers:")
    print("1. France (FranceScraper)")
    print("\nTo create a new scraper:")
    print("1. Copy this template")
    print("2. Create a new class inheriting from CountryScraper")
    print("3. Override get_template_data() with country-specific data")
    print("4. Run the scraper")
    print("\n" + "=" * 80)

    # Example: Run France scraper
    print("\nRunning France scraper as example...")
    scraper = FranceScraper()
    data = scraper.scrape_all()
    scraper.save_to_json(data)

    print("\n✅ Check resources/france_new.json")


if __name__ == "__main__":
    main()
