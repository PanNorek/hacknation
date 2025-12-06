import os

from dotenv import load_dotenv
from pydantic_ai import Agent
from pydantic_ai.models.google import GoogleModel
from pydantic_ai.providers.google import GoogleProvider

from src.configuration import Configuration
from src.models.output import Output, Reason

load_dotenv()

DEFAULT_MODEL = "gemini-2.0-flash"
API_KEY_NAME = "GOOGLE_API_KEY"
API_KEY = os.getenv(API_KEY_NAME)

provider = GoogleProvider(api_key=API_KEY)
model = GoogleModel(DEFAULT_MODEL, provider=provider)

agent = Agent(
    output_type=Output,
    model=model,
    system_prompt="""
    You are a helpful AI assistant powered by Google's Gemini.

    Your capabilities include:
    - Answering questions accurately and comprehensively
    - Providing detailed explanations
    - Helping with problem-solving
    - Offering creative suggestions
    - Maintaining helpful and friendly communication

    Always strive to be:
    - Accurate and truthful
    - Clear and concise in your responses
    - Helpful and engaging
    - Respectful and professional

    If you don't know something, admit it rather than making up information.
    """,
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
        "model": "gemini-2.0-flash",
        "provider": "Google",
        "capabilities": ["text_generation", "conversation", "problem_solving"],
        "system_prompt": agent.system_prompt,
    }
