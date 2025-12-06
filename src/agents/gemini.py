from google.genai.types import HarmBlockThreshold, HarmCategory
from pydantic_ai import Agent
from pydantic_ai.models.google import GoogleModel, GoogleModelSettings
from pydantic_ai.providers.google import GoogleProvider

from src.configuration import Configuration
from src.helpers import load_system_prompt
from src.models.output import Output, Reason
from src.models.input import CountryInput

# Load configuration
config = Configuration()

PROMPT_PATH = "src/agents/prompt.md"

provider = GoogleProvider(api_key=config.google_api_key.get_secret_value())

settings = GoogleModelSettings(
    temperature=config.temperature,
    max_tokens=config.max_tokens,
    google_safety_settings=[
        {
            "category": HarmCategory.HARM_CATEGORY_HATE_SPEECH,
            "threshold": HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
        }
    ],
)

model = GoogleModel(config.google_model_name, provider=provider, settings=settings)


agent = Agent(
    output_type=Output,
    model=model,
    system_prompt=load_system_prompt(PROMPT_PATH),
)


async def ask_gemini(prompt: str, form: CountryInput) -> Output:
    """
    Send a prompt to the Gemini agent and get a response.

    Args:
        prompt: The user's question or request

    Returns:
        The agent's response as an Output object
    """
    user_prompt = f"User prompt: {prompt}\n\nForm: {form.model_dump_json()}"

    try:
        result = await agent.run(user_prompt)
        return result.output
    except Exception as e:
        raise Exception(f"Error: {str(e)}")


def get_agent_info() -> dict:
    """
    Get information about the Gemini agent.

    Returns:
        Dictionary with agent information
    """
    return {
        "model": config.google_model_name,
        "provider": "Google",
        "capabilities": ["text_generation", "conversation", "problem_solving"],
        "system_prompt": agent.system_prompt,
    }
