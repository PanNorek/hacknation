from google.adk.agents import Agent
from google.adk.apps.app import App
from google.adk.tools.google_search_tool import google_search

DEFAULT_MODEL = "gemini-2.0-flash"

root_agent = Agent(
    model=DEFAULT_MODEL,
    name="agento",
    description="Short description of the agent",
    instruction="Instructions for the agent's behavior",
    tools=[google_search],  # Google search tool included by default
)

app = App(
    name="test_agent_new",
    root_agent=root_agent,
)
