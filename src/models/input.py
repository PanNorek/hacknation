from typing import List

from pydantic import BaseModel


class CountryInput(BaseModel):
    country_name: str | None
    geographical_features: str | None
    population: str | None
    climate: str | None
    economic_strengths: str | None
    army_size: str | None
    digitalization_level: str | None
    currency: str | None
    key_bilateral_relations: List[str] | None
    political_economic_threats: str | None
    military_threats: str | None
    development_milestones: str | None
