from fastapi import APIRouter
from pydantic import BaseModel

from src.configuration import Configuration
from src.helpers import load_system_prompt

config = Configuration()

router = APIRouter()


class AgentInfoResponse(BaseModel):
    model: str
    provider: str
    capabilities: list
    system_prompt: str


@router.get("/agent_info", tags=["agent_info"])
async def agent_info():
    return AgentInfoResponse(
        model=config.google_model_name,
        provider="Google",
        capabilities=["text_generation", "conversation", "problem_solving"],
        system_prompt=load_system_prompt("src/prompts/root.md"),
    ).model_dump(mode="json")
