from google.adk.agents import Agent
from google.adk.apps.app import App
from google.adk.tools.google_search_tool import google_search

PROMPT_PATH = "google_adk_agents/internet_searcher/prompt.md"
DEFAULT_MODEL = "gemini-2.5-flash-lite"


def load_system_prompt(file_path: str) -> str:
    """Load the system prompt for AI agent from a specified file."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError as e:
        raise FileExistsError("Error: System prompt file not found.") from e


root_agent = Agent(
    model=DEFAULT_MODEL,
    name="internet_searcher_agent",
    description="An AI agent that can perform internet searches using Google Search to answer user queries.",
    static_instruction=load_system_prompt(PROMPT_PATH),
    tools=[google_search],  # Google search tool included by default
)

app = App(
    name="test_agent_new",
    root_agent=root_agent,
)
