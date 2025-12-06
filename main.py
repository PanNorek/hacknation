import asyncio

from src.agents.agent.gemini import ask_gemini, get_agent_info
from src.configuration import Configuration
from src.models.input import CountryInput

input_data = {
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


async def test_gemini_agent():
    """Test the Gemini agent with a simple prompt."""
    try:
        # Test basic functionality
        prompt = f"How many soldiers does Atlantis have? {input_data}"
        print(f"Prompt: {prompt}")

        response = await ask_gemini(prompt)
        print(f"Response: {response.response}")
        print(f"Confidence: {response.confidence}")
        print("Reasoning:")
        for reason in response.reasoning:
            print(
                f"  - {reason.title}: {reason.description} (confidence: {reason.confidence})"
            )

    except Exception as e:
        print(f"Error testing Gemini agent: {e}")


if __name__ == "__main__":
    # Test CountryInput validation
    print("Testing CountryInput validation...")
    try:
        country_input = CountryInput(**input_data)
        print("✓ CountryInput validation successful!")
        print(f"Country: {country_input.country_name}")
        print(f"Population: {country_input.population}")
        print(f"Climate: {country_input.climate}")
        print(f"Key relations: {', '.join(country_input.key_bilateral_relations)}")
    except Exception as e:
        print(f"✗ CountryInput validation failed: {e}")

    # Test configuration
    print("\n" + "=" * 50)
    # configuration = Configuration()
    # print("Configuration loaded successfully!")
    # print(f"API Key configured: {configuration.gemini_api_key is not None}")

    # Test agent info
    agent_info = get_agent_info()
    print(f"\nAgent Info: {agent_info}")

    # Run async test
    print("\nTesting Gemini agent...")
    asyncio.run(test_gemini_agent())
