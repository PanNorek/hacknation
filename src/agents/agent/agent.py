from google.adk.agents import Agent
from google.adk.tools import agent_tool
from google.adk.tools.google_search_tool import google_search

DEFAULT_MODEL = "gemini-2.5-flash"

INTERNET_SEARCHER_NAME = "internet_searcher_agent"
SUMMARIZER_NAME = "summarizer_agent"
ROOT_AGENT_NAME = "root_agent"

PROMPTS = {
    INTERNET_SEARCHER_NAME: "src/prompts/internet_searcher.md",
    ROOT_AGENT_NAME: "src/prompts/root.md",
}


def load_system_prompt(file_path: str) -> str:
    """Load the system prompt for AI agent from a specified file."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError as e:
        raise FileExistsError(f"System prompt file not found: {file_path}") from e


internet_searcher = Agent(
    model=DEFAULT_MODEL,
    name=INTERNET_SEARCHER_NAME,
    description="An AI agent that can perform internet searches using Google Search to answer user queries.",
    static_instruction=load_system_prompt(PROMPTS[INTERNET_SEARCHER_NAME]),
    tools=[google_search],
)

summarizer = Agent(
    model=DEFAULT_MODEL,
    name=SUMMARIZER_NAME,
    description="An AI agent that summarizes information about a country's future based on provided context.",
    static_instruction="You are a summarization agent that provides concise summaries based on the context given to you.",
)


root_agent = Agent(
    model=DEFAULT_MODEL,
    name=ROOT_AGENT_NAME,
    description="An AI agent specialized in predicting future of the country based on the context.",
    static_instruction=load_system_prompt(PROMPTS[ROOT_AGENT_NAME]),
    tools=[
        agent_tool.AgentTool(internet_searcher),
        agent_tool.AgentTool(summarizer),
    ],
)
