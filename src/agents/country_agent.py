import mesa
import json
import asyncio
import logging
from datetime import datetime
from src.agents.forecasting_agent import generate_forecast

# Configure logging
logger = logging.getLogger(__name__)

class CountryAgent(mesa.Agent):
    """
    An agent representing a country in the simulation.
    """

    def __init__(self, model:mesa.Model, name:str):
        super().__init__(model)
        self.state = "exploring"
        self.explored_countries = []
        self.forecasts = None

        self.load_description(name)

    
    def load_description(self, name:str):
        """
        Load initial resources for the Country agent.
        """
        with open(f'resources/{name.lower()}.json', 'r') as file:
            resources = json.load(file)
        self.resources = resources



    def step(self):
        """
        Define the agent's behavior for a single step in the simulation.
        """
        if self.state == "exploring":
            self.explore()
        elif self.state == "forecast_scenario":
            self.forecast_scenario()
        elif self.state == "done":
            pass

    def explore(self):
        """
        Logic for exploring the environment and other agents resources.
        """
        logger.info(f"{self.resources['country_name']} is exploring other countries...")
        
        # Get all agents from the model
        for agent in self.model.my_agents:
            # Skip self
            if agent == self:
                continue
            
            # Store explored country data
            self.explored_countries.append(agent.resources)
            logger.debug(f"{self.resources['country_name']} discovered {agent.resources['country_name']}")
        
        # After exploration, transition to forecasting
        logger.info(f"{self.resources['country_name']} finished exploration. Ready for forecasting.")
        self.state = "forecast_scenario"
    
    def forecast_scenario(self):
        """
        Logic for forecasting scenarios using Gemini AI.
        Generates 12-month and 36-month forecasts with positive and negative scenarios.
        """
        if not hasattr(self.model, 'scenario') or not self.model.scenario:
            logger.warning(f"{self.resources['country_name']}: No scenario available for forecasting.")
            return
        
        logger.info("="*80)
        logger.info(f"{self.resources['country_name']} is generating forecasts...")
        
        try:
            # Get or create event loop
            try:
                loop = asyncio.get_event_loop()
                if loop.is_closed():
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
            
            # Run async forecast generation
            scenario_weight = self.model.scenario.get('total_weight', self.model.scenario.get('weight', 100))
            self.forecasts = loop.run_until_complete(generate_forecast(
                country_name=self.resources['country_name'],
                country_resources=self.resources,
                other_countries=self.explored_countries,
                scenario=self.model.scenario['description'],
                scenario_weight=scenario_weight
            ))
            
            # Log completion with summary
            logger.info("="*80)
            logger.info(f"FORECAST GENERATED FOR {self.resources['country_name']}")
            logger.info(f"12-month confidence: {self.forecasts.forecast_12_months.confidence:.2f}")
            logger.info(f"36-month confidence: {self.forecasts.forecast_36_months.confidence:.2f}")
            logger.info("="*80)
            
            # After forecasting, stop further steps
            self.state = "done"
            
        except Exception as e:
            logger.error(f"Error generating forecast for {self.resources['country_name']}: {e}")
            logger.error(f"Error type: {type(e).__name__}")
            if "name resolution" in str(e).lower():
                logger.error("This appears to be a network/DNS issue. Check your internet connection.")
            elif "api key" in str(e).lower() or "GOOGLE_API_KEY" in str(e):
                logger.error("Make sure GOOGLE_API_KEY is set in your .env file.")
            self.state = "done"