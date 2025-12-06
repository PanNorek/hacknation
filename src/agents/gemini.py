import os

from dotenv import load_dotenv
from google.genai.types import HarmBlockThreshold, HarmCategory
from pydantic_ai import Agent
from pydantic_ai.models.google import GoogleModel, GoogleModelSettings
from pydantic_ai.providers.google import GoogleProvider

from src.configuration import Configuration
from src.helpers import load_system_prompt
from src.models.output import Output, Reason

load_dotenv()

PROMPT_PATH = "src/agents/prompt.md"
DEFAULT_MODEL = "gemini-2.0-flash"
API_KEY_NAME = "GOOGLE_API_KEY"
API_KEY = os.getenv(API_KEY_NAME)


provider = GoogleProvider(api_key=API_KEY)

settings = GoogleModelSettings(
    temperature=0.2,
    max_tokens=1024,
    google_safety_settings=[
        {
            "category": HarmCategory.HARM_CATEGORY_HATE_SPEECH,
            "threshold": HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
        }
    ],
)

model = GoogleModel(DEFAULT_MODEL, provider=provider, settings=settings)


agent = Agent(
    output_type=Output,
    model=model,
    system_prompt=load_system_prompt(PROMPT_PATH),
)


async def ask_gemini(prompt: str) -> Output:
    """
    Send a prompt to the Gemini agent and get a response.

    Args:
        prompt: The user's question or request

    Returns:
        The agent's response as an Output object
    """
    try:
        result = await agent.run(prompt)
        print(result.output)
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
        "model": DEFAULT_MODEL,
        "provider": "Google",
        "capabilities": ["text_generation", "conversation", "problem_solving"],
        "system_prompt": agent.system_prompt,
    }
