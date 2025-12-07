from typing import List

from pydantic import BaseModel, Field


class CountryInput(BaseModel):
    """Country information extraction schema - simplified for Google ADK compatibility."""

    country_name: str = Field(default="", description="The name of the country")
    geographical_features: str = Field(
        default="", description="Key geographical features and location characteristics"
    )
    population: str = Field(
        default="", description="Population size and demographic information"
    )
    climate: str = Field(default="", description="Climate type and weather patterns")
    economic_strengths: str = Field(
        default="", description="Major economic sectors, industries, and strengths"
    )
    army_size: str = Field(
        default="", description="Military force size and capabilities"
    )
    digitalization_level: str = Field(
        default="",
        description="Level of technological and digital infrastructure adoption",
    )
    currency: str = Field(
        default="", description="Official currency used by the country"
    )
    key_bilateral_relations: List[str] = Field(
        default=[],
        description="List of key bilateral relationships with other countries",
    )
    political_economic_threats: str = Field(
        default="", description="Current political and economic challenges or threats"
    )
    military_threats: str = Field(
        default="", description="Military security concerns and defense challenges"
    )
    development_milestones: str = Field(
        default="", description="Major historical achievements and development progress"
    )
