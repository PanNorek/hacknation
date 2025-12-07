from typing import List

from google.adk.agents import Agent, SequentialAgent
from google.adk.tools.agent_tool import AgentTool
from google.adk.tools.google_search_tool import google_search
from pydantic import BaseModel, Field

from src.models.input import CountryInput
from src.agents.tools.embedding_search import embeddings_search, EmbeddingsSearchOutput


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
    output_key="search_results",
)

summarizer = Agent(
    model=DEFAULT_MODEL,
    name=SUMMARIZER_NAME,
    output_key="summary",
    description="An AI agent that synthesizes internet search results into actionable insights about threats and opportunities for a country.",
    static_instruction=""" Your task:

1. **Analyze** the search results in the context of the country's profile
2. **Categorize** findings into:
   - **Threats**: Risks to security, economy, stability, or international position
   - **Opportunities**: Potential advantages for growth, partnerships, or strategic gains
3. **Output Format**:
   - Use clear bullet points
   - Each point should be concise (1-2 sentences)
   - Include timeframe when relevant (recent, ongoing, upcoming)
   - Prioritize by impact level (high/medium/low)

**Structure your response:**
## Threats
- [High Impact] Threat description with context
- [Medium Impact] Threat description with context

## Opportunities
- [High Impact] Opportunity description with context
- [Medium Impact] Opportunity description with context

Be specific, actionable, and factual. Focus on geopolitical, economic, and security implications.""",
)

extractor = Agent(
    output_schema=CountryInput,
    model=DEFAULT_MODEL,
    name=EXTRACTOR_TOOL_NAME,
    description="An AI agent that extracts information about a country from the user's question.",
    static_instruction="""You are a extraction agent that converts raw information provide by user
    into structured data about a country. Extract as much information as possible.
    If some information is missing you can skip it""",
)

final_formatter = Agent(
    output_schema=Output,
    model=DEFAULT_MODEL,
    name="final_formatter",
    description="An AI agent that formats the final analysis into structured output with confidence and reasoning",
    static_instruction=load_system_prompt(PROMPTS[ROOT_AGENT_NAME]),
)


embeddings_searcher = Agent(
    output_schema=EmbeddingsSearchOutput,
    model=DEFAULT_MODEL,
    name="embeddings_searcher",
    description="An AI agent that searches for information about a country from the embeddings database.",
    static_instruction="""You are a embeddings searcher agent that searches for information about a country from the embeddings database""",
    tools=[embeddings_search],
)


root_agent = Agent(
    output_schema=Output,
    model=DEFAULT_MODEL,  # Add model parameter
    name=ROOT_AGENT_NAME,
    description="Sequential pipeline that always processes country analysis in order: extract country data, search for threats/opportunities, summarize findings, and format final output.",
    static_instruction=load_system_prompt(PROMPTS[ROOT_AGENT_NAME]),
    tools=[
        AgentTool(extractor),
        AgentTool(internet_searcher),
        AgentTool(embeddings_searcher),
        AgentTool(summarizer),
        AgentTool(final_formatter),
    ],
)
# root_agent = SequentialAgent(
#     name=ROOT_AGENT_NAME,
#     description="Sequential pipeline that always processes country analysis in order: extract country data, search for threats/opportunities, summarize findings, and format final output.",
#     sub_agents=[
#         extractor,
#         internet_searcher,
#         embeddings_searcher,
#         summarizer,
#         final_formatter,
#     ],
# )
