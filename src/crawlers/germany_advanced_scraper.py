#!/usr/bin/env python3
"""
Advanced Germany Government Websites Scraper
Crawls official German government websites and uses LLM to extract structured data
"""
import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

import requests
from bs4 import BeautifulSoup
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional
from urllib.parse import urljoin, urlparse
import time
import asyncio
from src.configuration import Configuration
from pydantic import BaseModel, Field
from pydantic_ai import Agent
from pydantic_ai.models.google import GoogleModel, GoogleModelSettings
from pydantic_ai.providers.google import GoogleProvider

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load configuration
config = Configuration()


class CountryData(BaseModel):
    """Structured country data model"""
    country_name: str = Field(default="Germany")
    geographical_features: str = Field(description="Geographical location and features")
    population: str = Field(description="Current population estimate")
    climate: str = Field(description="Climate description")
    economic_strengths: str = Field(description="Key economic sectors and strengths")
    army_size: str = Field(description="Military personnel size")
    digitalization_level: str = Field(description="Level of digitalization and tech adoption")
    currency: str = Field(default="Euro (EUR)")
    key_bilateral_relations: List[str] = Field(description="List of key partner countries")
    political_economic_threats: str = Field(description="Current political and economic challenges")
    military_threats: str = Field(description="Security and military threats")
    development_milestones: str = Field(description="Recent and planned development achievements")
    sources: List[Dict] = Field(default_factory=list, description="Data sources with URLs")
    last_updated: str = Field(default_factory=lambda: datetime.now().isoformat())
    scraped_content_summary: Dict[str, str] = Field(default_factory=dict, description="Summary of scraped content per URL")


class GermanyGovernmentScraper:
    """Advanced scraper for German government websites"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
        })
        
        self.start_urls = start_urls = [
    # rząd, ministerstwa, administracja
    "https://www.auswaertiges-amt.de/en",              # Foreign Affairs
    "https://www.bmvg.de/en",                          # Defence Ministry
    "https://www.bmwk.de/Redaktion/EN/Dossier/dossier.html",  # Economy & Climate / Industry
    "https://www.bmi.bund.de/EN/home/home_node.html",  # Interior Ministry
    "https://www.bmbf.de/bmbf/en/home/home_node.html", # Education & Research
    "https://www.bmuv.de/EN/home/home_node.html",      # Environment / Climate / Energy
    "https://www.digital-strategy.de/en",              # Digital Strategy & ICT policy

    # Statystyki, dane demograficzne, PKB, ekonomia
    "https://www.destatis.de/EN/Home/_node.html",     # Federal Statistical Office — statystyki różnych sektorów

    # Giełda i rynek finansowy
    "https://www.deutsche-boerse.com/dbg-en/",          # Deutsche Börse (giełda, rynki, indeksy)
    "https://tradingeconomics.com/germany/stock-market",# indeksy giełdowe & dane rynku Niemieckiego
    "https://www.investing.com/indices/germany-40",     # alternatywne źródło notowań

    # Ogólna charakterystyka kraju, geografia, społeczeństwo
    "https://en.wikipedia.org/wiki/Germany",           # Wikipedia — dobry punkt wyjścia do mixu danych

    # Źródła gospodarcze / makroekonomia / analizy
    "https://www.icao.int/globalairnavigationplan/",   # (jeśli potrzebujesz np. transportu i infrastruktury — przykład),
    # możesz dodać inne think‑tanki lub instytuty ekonomiczne

    # Ewentualne instytucje finansowe / analizy rynku
    # (tu można dodać np. Bundesbank, BMF etc. jeśli mają publiczne raporty)
]
        
        self.scraped_content = {}
        self.max_pages_per_domain = 3  # Limit pages per domain to avoid overload
        self.delay_between_requests = 2  # Seconds
        
        # Setup LLM
        self._setup_llm()
    
    def _setup_llm(self):
        """Setup Gemini LLM for data extraction"""
        api_key = config.gemini_api_key
        if not api_key:
            raise ValueError("GEMINI_API_KEY not set in configuration")
        
        provider = GoogleProvider(api_key=api_key)
        settings = GoogleModelSettings(
            temperature=0.1,  # Low temperature for factual extraction
            max_tokens=4096,
        )
        model = GoogleModel(config.gemini_model_name, provider=provider, settings=settings)
        
        system_prompt = """
You are an expert data analyst specialized in extracting structured information about countries from government websites.

Your task is to analyze scraped content from German government websites and extract accurate, factual information.

IMPORTANT RULES:
1. Extract ONLY factual information present in the provided content
2. If information is not available or unclear, use exactly this phrase: "NOT_FOUND"
3. Be concise but comprehensive
4. For lists (like key_bilateral_relations), extract all mentioned countries
5. Focus on recent/current information (2023-2025)
6. Use official numbers and data when available
7. Synthesize information from multiple sources if provided

CRITICAL: Use "NOT_FOUND" (exactly this string) for any field where you cannot find reliable information in the scraped content.
This allows the system to preserve existing data instead of overwriting with guesses.

OUTPUT FORMAT:
All fields must be filled. If you cannot find information, use "NOT_FOUND" as the value.
"""
        
        self.llm_agent = Agent(
            output_type=CountryData,
            model=model,
            system_prompt=system_prompt
        )
    
    def scrape_url(self, url: str, max_depth: int = 1) -> Dict[str, str]:
        """
        Scrape a URL and extract text content
        
        Args:
            url: URL to scrape
            max_depth: How many levels deep to follow links (0 = just this page)
            
        Returns:
            Dictionary with URL as key and extracted text as value
        """
        logger.info(f"Scraping: {url}")
        
        try:
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script, style, and navigation elements
            for element in soup(['script', 'style', 'nav', 'header', 'footer']):
                element.decompose()
            
            # Extract main content
            main_content = soup.find('main') or soup.find('article') or soup.find('body')
            
            if main_content:
                text = main_content.get_text(separator=' ', strip=True)
                # Clean up whitespace
                text = ' '.join(text.split())
                
                # Limit text length to avoid token limits
                if len(text) > 10000:
                    text = text[:10000] + "... (truncated)"
                
                return {url: text}
            
            return {url: "No content extracted"}
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error scraping {url}: {e}")
            return {url: f"Error: {str(e)}"}
        except Exception as e:
            logger.error(f"Unexpected error scraping {url}: {e}")
            return {url: f"Error: {str(e)}"}
    
    def scrape_all_sources(self) -> Dict[str, str]:
        """
        Scrape all configured URLs
        
        Returns:
            Dictionary mapping URLs to extracted content
        """
        logger.info("="*80)
        logger.info("Starting comprehensive scraping of German government websites")
        logger.info("="*80)
        
        all_content = {}
        
        for idx, url in enumerate(self.start_urls, 1):
            logger.info(f"[{idx}/{len(self.start_urls)}] Processing: {url}")
            
            content = self.scrape_url(url)
            all_content.update(content)
            
            # Respectful delay between requests
            if idx < len(self.start_urls):
                logger.info(f"Waiting {self.delay_between_requests}s before next request...")
                time.sleep(self.delay_between_requests)
        
        logger.info("="*80)
        logger.info(f"Scraping complete: {len(all_content)} pages collected")
        logger.info("="*80)
        
        return all_content
    
    async def extract_structured_data(self, scraped_content: Dict[str, str], existing_data_path: str = "resources/germany.json") -> CountryData:
        """
        Use LLM to extract structured data from scraped content
        
        Args:
            scraped_content: Dictionary of URL -> content
            existing_data_path: Path to existing JSON file with current data
            
        Returns:
            CountryData object with extracted information
        """
        logger.info("="*80)
        logger.info("Using LLM to extract structured data...")
        logger.info("="*80)
        
        # Load existing data if available
        existing_data = {}
        if Path(existing_data_path).exists():
            try:
                with open(existing_data_path, 'r', encoding='utf-8') as f:
                    existing_data = json.load(f)
                logger.info(f"📂 Loaded existing data from {existing_data_path}")
            except Exception as e:
                logger.warning(f"Could not load existing data: {e}")
        else:
            logger.info("No existing data found - will create new entry")
        
        # Prepare content summary
        content_summary = []
        for url, content in scraped_content.items():
            domain = urlparse(url).netloc
            content_preview = content[:500] if len(content) > 500 else content
            content_summary.append(f"\n--- SOURCE: {domain} ({url}) ---\n{content_preview}\n")
        
        combined_content = "\n".join(content_summary)
        
        # Create prompt for LLM with existing data context
        existing_data_str = json.dumps(existing_data, indent=2) if existing_data else "No existing data"
        
        prompt = f"""
You are updating the existing database entry for Germany with fresh information from government websites.

EXISTING DATA (CURRENT DATABASE):
{existing_data_str}

NEW SCRAPED CONTENT:
{combined_content[:12000]}  # Limit to avoid token overflow

TASK:
Review the NEW SCRAPED CONTENT and update ONLY the fields where you found NEW, RELIABLE information.

For each field:
1. **geographical_features**: Location, borders, terrain
2. **population**: Current population estimate (use latest available data)
3. **climate**: Climate description
4. **economic_strengths**: Key industries, economic sectors, GDP info
5. **army_size**: Size of Bundeswehr (German armed forces)
6. **digitalization_level**: Digital transformation, Industry 4.0, tech adoption
7. **currency**: Official currency
8. **key_bilateral_relations**: List of key partner countries mentioned
9. **political_economic_threats**: Current challenges (energy, economy, demographics, etc.)
10. **military_threats**: Security threats, defense concerns
11. **development_milestones**: Recent achievements and future plans

CRITICAL RULES:
- If you found NEW information in the scraped content that updates/improves the existing data → USE THE NEW DATA
- If the scraped content has NO information about a field → Return exactly "NOT_FOUND" for that field
- If the existing data is already good and scraped content has nothing new → Return "NOT_FOUND" to preserve existing
- DO NOT guess or infer
- DO NOT copy existing data - let the system preserve it automatically
- Focus on RECENT information (2024-2025) when available
- Use official statistics and numbers

EXAMPLES:
- Existing army_size: "183,000" | Scraped: mentions "185,000 active personnel" → UPDATE to "185,000"
- Existing population: "84,000,000" | Scraped: no population mentioned → Return "NOT_FOUND" (preserve existing)
- Existing climate: "good data" | Scraped: no climate info → Return "NOT_FOUND"

Remember: "NOT_FOUND" tells the system to KEEP the existing value. Only provide new data when you actually found something useful!
"""
        
        try:
            result = await self.llm_agent.run(prompt)
            country_data = result.output
            
            # Add sources
            country_data.sources = [
                {
                    'url': url,
                    'domain': urlparse(url).netloc,
                    'scraped_at': datetime.now().isoformat(),
                    'content_length': len(content)
                }
                for url, content in scraped_content.items()
            ]
            
            # Add content summaries
            country_data.scraped_content_summary = {
                urlparse(url).netloc: f"{len(content)} characters extracted"
                for url, content in scraped_content.items()
            }
            
            logger.info("✅ Structured data extracted successfully")
            return country_data
            
        except Exception as e:
            logger.error(f"Error extracting structured data with LLM: {e}")
            raise
    
    def save_to_json(self, data: CountryData, filepath: str = "resources/germany.json"):
        """
        Save structured data to JSON file (clean, without metadata)
        Only updates fields that were successfully found - preserves existing data for NOT_FOUND fields
        """
        try:
            # Load existing data if file exists
            existing_data = {}
            if Path(filepath).exists():
                with open(filepath, 'r', encoding='utf-8') as f:
                    existing_data = json.load(f)
                logger.info(f"📂 Loaded existing data from {filepath}")
            else:
                logger.info(f"📝 Creating new file: {filepath}")
            
            # Convert Pydantic model to dict
            data_dict = data.model_dump()
            
            # Define fields to keep in final output (no sources, no metadata)
            clean_fields = [
                "country_name",
                "geographical_features",
                "population",
                "climate",
                "economic_strengths",
                "army_size",
                "digitalization_level",
                "currency",
                "key_bilateral_relations",
                "political_economic_threats",
                "military_threats",
                "development_milestones"
            ]
            
            # Start with existing data
            clean_data = existing_data.copy()
            
            # Update only fields that were successfully found (not "NOT_FOUND")
            updated_fields = []
            preserved_fields = []
            
            for field in clean_fields:
                new_value = data_dict.get(field, "")
                
                # Check if field was found
                if field == "key_bilateral_relations":
                    # Special handling for lists
                    if isinstance(new_value, list) and new_value and "NOT_FOUND" not in str(new_value):
                        clean_data[field] = new_value
                        updated_fields.append(field)
                    elif field in existing_data:
                        # Preserve existing list
                        preserved_fields.append(field)
                    else:
                        # New field, empty list
                        clean_data[field] = []
                else:
                    # String fields
                    if new_value and new_value != "NOT_FOUND" and "NOT_FOUND" not in new_value:
                        clean_data[field] = new_value
                        updated_fields.append(field)
                    elif field in existing_data:
                        # Preserve existing value
                        preserved_fields.append(field)
                    else:
                        # New field, empty string
                        clean_data[field] = ""
            
            # Ensure all required fields exist
            for field in clean_fields:
                if field not in clean_data:
                    if field == "key_bilateral_relations":
                        clean_data[field] = []
                    else:
                        clean_data[field] = ""
            
            # Save updated data
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(clean_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"✅ Data saved to {filepath}")
            logger.info(f"   📝 Updated fields ({len(updated_fields)}): {', '.join(updated_fields)}")
            if preserved_fields:
                logger.info(f"   💾 Preserved existing data ({len(preserved_fields)}): {', '.join(preserved_fields)}")
            
        except Exception as e:
            logger.error(f"Error saving data: {e}")
            raise
    
    def save_raw_content(self, content: Dict[str, str], filepath: str = "resources/germany_raw_content.json"):
        """Save raw scraped content for debugging"""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(content, f, indent=2, ensure_ascii=False)
            
            logger.info(f"✅ Raw content saved to {filepath}")
            
        except Exception as e:
            logger.error(f"Error saving raw content: {e}")
    
    @staticmethod
    def cleanup_interim_files():
        """Delete interim/temporary files after successful completion"""
        import os
        
        interim_files = [
            "resources/germany_raw_content.json",
            "resources/germany_new.json"
        ]
        
        for filepath in interim_files:
            if os.path.exists(filepath):
                try:
                    os.remove(filepath)
                    logger.info(f"🗑️  Deleted interim file: {filepath}")
                except Exception as e:
                    logger.warning(f"Could not delete {filepath}: {e}")


async def main():
    """Main function to run the advanced scraper"""
    logger.info("="*80)
    logger.info("ADVANCED GERMANY GOVERNMENT SCRAPER")
    logger.info("="*80)
    
    scraper = GermanyGovernmentScraper()
    
    # Step 1: Scrape all sources
    scraped_content = scraper.scrape_all_sources()
    
    # Save raw content for debugging
    scraper.save_raw_content(scraped_content)
    
    # Step 2: Extract structured data using LLM
    country_data = await scraper.extract_structured_data(scraped_content)
    
    # Step 3: Print summary
    print("\n" + "="*80)
    print("EXTRACTED DATA SUMMARY")
    print("="*80)
    print(f"Country: {country_data.country_name}")
    print(f"Population: {country_data.population}")
    print(f"Army Size: {country_data.army_size}")
    print(f"Economic Strengths: {country_data.economic_strengths[:100]}...")
    print(f"Digitalization Level: {country_data.digitalization_level[:100]}...")
    print(f"Key Relations: {', '.join(country_data.key_bilateral_relations[:5])}")
    print(f"\nSources scraped: {len(country_data.sources)}")
    for source in country_data.sources:
        print(f"  - {source['domain']}")
    
    # Step 4: Save to file (clean data only)
    scraper.save_to_json(country_data)
    
    # Step 5: Clean up interim files
    logger.info("\nCleaning up interim files...")
    scraper.cleanup_interim_files()
    
    print("\n" + "="*80)
    print("✅ SCRAPING AND EXTRACTION COMPLETE!")
    print("="*80)
    print(f"📄 Final structured data: resources/germany.json")
    print(f"🗑️  Interim files cleaned up")
    print("="*80)


if __name__ == "__main__":
    asyncio.run(main())
