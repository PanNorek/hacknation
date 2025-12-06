from typing import List

from pydantic import BaseModel


class CountryInput(BaseModel):
    country_name: str
    geographical_features: str
    population: str
    climate: str
    economic_strengths: str
    army_size: str
    digitalization_level: str
    currency: str
    key_bilateral_relations: List[str]
    political_economic_threats: str
    military_threats: str
    development_milestones: str
