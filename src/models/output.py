from typing import List

from pydantic import BaseModel, Field


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
        min_length=2, max_length=4, description="The sources of the response"
    )
