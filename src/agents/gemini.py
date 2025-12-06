from pydantic_ai import Agent
from pydantic_ai.models.gemini import GeminiModel
from ..configuration import Configuration
from ..models.output import Output, Reason
from pydantic_ai.providers.google_gla import GoogleGLAProvider


# Initialize the Gemini model
# google_gla_provider = GoogleGLAProvider(api_key=Configuration().gemini_api_key)
# model = GeminiModel(model_name="gemini-1.5-flash", provider=google_gla_provider)

# Create the Gemini agent
gemini_agent = Agent(
    output_type=Output,
    model="gemini-2.0-flash",
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
        result = await gemini_agent.run(prompt)
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
        "system_prompt": gemini_agent.system_prompt,
    }
