from typing import List

from google.adk.agents import Agent, SequentialAgent
from google.adk.tools import agent_tool
from google.adk.tools.google_search_tool import google_search
from pydantic import BaseModel, Field
from src.models.input import CountryInput


class Reason(BaseModel):
    title: str
    description: str
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)


class Output(BaseModel):
    response: str = Field(description="The response to the user's question")
    confidence: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
        description="The confidence in the response between 0 and 1",
    )
    reasoning: List[Reason] = Field(
        min_length=2, max_length=6, description="The sources of the response"
    )


DEFAULT_MODEL = "gemini-2.5-flash"

EXTRACTOR_TOOL_NAME = "extractor_tool"
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
    input_schema=CountryInput,
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

extractorTool = Agent(
    output_schema=CountryInput,
    model=DEFAULT_MODEL,
    name=EXTRACTOR_TOOL_NAME,
    description="An AI agent that extracts information about a country from the user's question. You should always start with this tool.",
    static_instruction="You are a extraction agent that prepares the information for the summarizer agent. If some information is missing you can skipp it",
)


seq_agent = SequentialAgent(
    name=ROOT_AGENT_NAME,
    description="An AI agent specialized in predicting future of the country based on the context. You should always start with extractor_tool the information from the user's question.",
    sub_agents=[
        extractorTool,
        internet_searcher,
        summarizer,
    ],
)
root_agent = Agent(
    model=DEFAULT_MODEL,
    name=ROOT_AGENT_NAME,
    description="An AI agent specialized in predicting future of the country based on the context. You should always start with extractor_tool the information from the user's question.",
    static_instruction=load_system_prompt(PROMPTS[ROOT_AGENT_NAME]),
    tools=[
        agent_tool.AgentTool(seq_agent),
    ],
    output_schema=Output,
)
