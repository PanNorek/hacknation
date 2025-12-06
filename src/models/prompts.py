from pydantic import BaseModel


class PromptRequest(BaseModel):
    prompt: str


class SystemInstructionInput(BaseModel):
    instruction: str
    description: str | None = None
