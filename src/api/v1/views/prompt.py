from fastapi import APIRouter
from pydantic import BaseModel
from src.agents.gemini import ask_gemini
from src.models.input import CountryInput

router = APIRouter()


class PromptRequest(BaseModel):
    prompt: str


@router.post("/prompt", tags=["prompt"])
async def prompt(prompt: PromptRequest):

    country_input = {
        "country_name": "Atlantis",
        "geographical_features": "access to the Baltic Sea, several large navigable rivers, limited drinking water resources",
        "population": "28 million",
        "climate": "temperate",
        "economic_strengths": "heavy industry, automotive, food, chemical, ICT, ambitions to play a significant role in renewable energy sources, processing critical raw materials and building supranational AI infrastructure (including big data centers, AI giga factories, quantum computers)",
        "army_size": "150 thousand professional soldiers",
        "digitalization_level": "above European average",
        "currency": "other than euro",
        "key_bilateral_relations": [
            "Germany",
            "France",
            "Finland",
            "Ukraine",
            "USA",
            "Japan",
        ],
        "political_economic_threats": "instability in the EU, disintegration of the EU into 'different speeds' groups in terms of development pace and interest in deeper integration; negative image campaign by several state actors aimed against the Atlantis government or society; disruptions in hydrocarbon fuel supplies from the USA, Scandinavia, Persian Gulf (resulting from potential changes in the internal policies of exporting countries or transport problems, e.g. Houthi attacks on tankers in the Red Sea); exposure to slowdown in ICT sector development due to embargo on advanced processors",
        "military_threats": "threat of armed attack by one of the neighbors; ongoing hybrid attacks by at least one neighbor for many years, including in the area of critical infrastructure and cyberspace",
        "development_milestones": "parliamentary democracy for 130 years; periods of economic stagnation in 1930-1950 and 1980-1990; EU and NATO membership since 1997; 25th largest economy in the world by GDP since 2020; budget deficit and public debt around EU average",
    }
    prompt_input = f"User prompt: {prompt.prompt}\n\nForm: {str(country_input)}"

    response = await ask_gemini(prompt_input)
    return response.model_dump(mode="json")
