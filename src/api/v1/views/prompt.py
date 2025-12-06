from fastapi import APIRouter
from pydantic import BaseModel

# from src.agents.root.gemini import ask_gemini
from src.models.input import CountryInput

router = APIRouter()


class PromptRequest(BaseModel):
    prompt: str
    form: CountryInput


# @router.post("/prompt", tags=["prompt"])
# async def prompt(prompt_request: PromptRequest):
#     response = await ask_gemini(prompt_request.prompt, prompt_request.form)
#     return response.model_dump(mode="json")
