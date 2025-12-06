from google.adk.agents import Agent

root_agent = Agent(
    model="gemini-2.0-flash",
    name="agent",
    description="Short description of the agent",
    instruction="Instructions for the agent's behavior",
    tools=[],
)
