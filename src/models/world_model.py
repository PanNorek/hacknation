# filepath: /home/rafal/coding/hacknation/src/models/world_model.py
"""
World Model for Diplomind
"""
import mesa
import os
import json
import logging
from typing import List, Dict, Optional
from src.agents.country_agent import CountryAgent

logger = logging.getLogger(__name__)


class WorldModel(mesa.Model):
    """
    Mesa model representing the world with countries as agents.
    Manages the simulation lifecycle: exploration → forecasting → reporting
    """
    
    def __init__(self, scenario: Optional[Dict] = None, resources_dir: str = 'resources'):
        """
        Initialize the World Model
        
        Args:
            scenario: Dictionary with 'description' and 'total_weight' keys.
                     If None, uses default complex scenario.
            resources_dir: Directory containing country JSON files
        """
        super().__init__()
        self.my_agents: List[CountryAgent] = []
        
        # Set scenario (use provided or default)
        if scenario is None:
            self.scenario = self._get_default_scenario()
        else:
            self.scenario = scenario
        
        # Load all countries from resources directory
        self._load_countries(resources_dir)
        
        logger.info(f"WorldModel initialized with {len(self.my_agents)} countries")
        logger.info(f"Scenario weight: {self.scenario.get('total_weight', 100)}/100")
    
    def _get_default_scenario(self) -> Dict:
        """
        Get the default complex multi-factor scenario
        
        Returns:
            Dictionary with scenario description and total_weight
        """
        return {
            "description": """
a) Wskutek zaistniałej przed miesiącem katastrofy naturalnej wiodący światowy producent procesorów graficznych stracił 60% zdolności produkcyjnych; odbudowa mocy produkcyjnych poprzez inwestycje w filie zlokalizowane na obszarach nieobjętych katastrofą potrwa do końca roku 2028 (waga istotności: 30)

b) Przemysł motoryzacyjny w Europie (piątka głównych partnerów handlowych państwa Atlantis to kraje europejskie) bardzo wolno przestawia się na produkcję samochodów elektrycznych; rynek europejski zalewają tanie samochody elektryczne z Azji Wschodniej; europejski przemysł motoryzacyjny będzie miał w roku 2025 zyski na poziomie 30% średnich rocznych zysków z lat 2020-2024 (waga istotności: 15)

c) PKB krajów strefy euro w roku 2025 spadnie średnio o 1,5% w stosunku do roku 2024 (waga istotności: 15)

d) Na wschodzie Ukrainy trwa słaby rozejm; Rosja kontroluje dwie główne elektrownie ukraińskie, które pracują na potrzeby konsumentów rosyjskich; gospodarka ukraińska rozwija się w tempie 4% PKB, głównie dzięki inwestycjom w przemysł zbrojeniowy i odbudowę infrastruktury (waga istotności: 10)

e) Inwestycje amerykańskie w Ukrainie kierowane są do przemysłu wydobywczego (surowce krytyczne); roczne inwestycje UE w Ukrainie są na poziomie 3% ukraińskiego PKB i utrzymają się na takim poziomie do roku 2029 (waga istotności: 5)

f) Mamy gwałtowny wzrost udziału energii z OZE w miksie energetycznym krajów UE oraz Chin od początku roku 2028; w połowie roku 2023 średniej wielkości kraj południowoamerykański odkrył ogromne i łatwe do eksploatacji złoża ropy naftowej i gazu ziemnego dorównujące wielkością złożom Arabii Saudyjskiej i Kataru, co przełoży się pod koniec roku 2027 na nadpodaż tych paliw na światowe rynki; wzrost podaży energii z OZE oraz nadpodaż paliw węglowodorowych przekładają się na znaczny spadek cen ropy: do poziomu 30-35 USD za baryłkę; będzie to miało wpływ na budżet Rosji oraz (w mniejszym stopniu) innych krajów producentów ropy i paliw ropopochodnych (waga istotności: 25)
            """.strip(),
            "total_weight": 100  # Sum of all scenario weights
        }
    
    def _load_countries(self, resources_dir: str):
        """
        Load all countries from JSON files in the resources directory
        
        Args:
            resources_dir: Path to directory containing country JSON files
        """
        if not os.path.exists(resources_dir):
            logger.error(f"Resources directory not found: {resources_dir}")
            raise FileNotFoundError(f"Resources directory not found: {resources_dir}")
        
        json_files = [f for f in os.listdir(resources_dir) if f.endswith('.json')]
        
        if not json_files:
            logger.warning(f"No country JSON files found in {resources_dir}")
            return
        
        for filename in json_files:
            try:
                filepath = os.path.join(resources_dir, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Create country agent
                country_name = data.get("country_name", filename[:-5])
                agent = CountryAgent(self, country_name)
                self.my_agents.append(agent)
                
                logger.debug(f"Loaded country: {country_name}")
                
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse JSON file {filename}: {e}")
            except Exception as e:
                logger.error(f"Failed to load country from {filename}: {e}")
    
    def step(self):
        """
        Execute one step of the simulation for all agents
        Each agent processes according to its current state:
        - exploring: Discover other countries
        - forecast_scenario: Generate AI forecasts
        - done: No action
        """
        for agent in self.my_agents:
            agent.step()
    
    def run_exploration(self):
        """Run the exploration phase - agents discover each other"""
        logger.info("="*80)
        logger.info("PHASE 1: EXPLORATION")
        logger.info("="*80)
        self.step()
    
    def run_forecasting(self):
        """Run the forecasting phase - agents generate AI forecasts"""
        logger.info("="*80)
        logger.info("PHASE 2: FORECASTING")
        logger.info("="*80)
        self.step()
    
    def run_simulation(self):
        """
        Run complete simulation: exploration + forecasting
        Convenience method that runs both phases
        """
        logger.info("Starting complete simulation")
        logger.info(f"Scenario preview: {self.scenario['description'][:200]}...")
        logger.info(f"Total Weight: {self.scenario['total_weight']}/100")
        
        self.run_exploration()
        self.run_forecasting()
        
        logger.info("="*80)
        logger.info("SIMULATION COMPLETE")
        logger.info("="*80)
    
    def get_forecasts(self) -> List[Dict]:
        """
        Collect all forecasts from agents
        
        Returns:
            List of dictionaries with 'country_name' and 'forecast' keys
        """
        forecasts_data = []
        for agent in self.my_agents:
            if agent.forecasts:
                forecasts_data.append({
                    'country_name': agent.resources['country_name'],
                    'forecast': agent.forecasts
                })
        
        logger.info(f"Collected forecasts from {len(forecasts_data)}/{len(self.my_agents)} countries")
        return forecasts_data
    
    def get_country_names(self) -> List[str]:
        """
        Get list of all country names in the simulation
        
        Returns:
            List of country names
        """
        return [agent.resources['country_name'] for agent in self.my_agents]
    
    def get_agent_by_country_name(self, country_name: str) -> Optional[CountryAgent]:
        """
        Get agent by country name
        
        Args:
            country_name: Name of the country
            
        Returns:
            CountryAgent or None if not found
        """
        for agent in self.my_agents:
            if agent.resources['country_name'] == country_name:
                return agent
        return None
    
    def __repr__(self):
        return f"WorldModel(countries={len(self.my_agents)}, scenario_weight={self.scenario.get('total_weight', 100)})"
