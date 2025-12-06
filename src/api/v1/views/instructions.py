import os
import json
import logging
from fastapi import APIRouter
from pydantic import BaseModel
from src.agents.gemini import ask_gemini
from src.models.input import CountryInput

logger = logging.getLogger(__name__)

router = APIRouter()


class InstructionsRequest(BaseModel):
    instructions: str


def save_instructions(data: InstructionsRequest):
    print(f"Saving instructions... {data}")
    # instructions_dir = os.Path(__file__).parent.parent.parent.parent / "instructions"
    instructions_dir = "./src/agents/instructions"
    if not os.path.exists(instructions_dir):
        os.makedirs(instructions_dir)
    with open(os.path.join(instructions_dir, "instructions.md"), "w") as f:
        json.dump(data.instructions, f)
        logger.info(f"Instructions saved to {instructions_dir}")


@router.post("/instructions", tags=["instructions"])
async def instructions(instructions: InstructionsRequest):

    save_instructions(instructions)
    return {"message": "Instructions saved successfully"}
