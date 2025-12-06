from fastapi import APIRouter
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from pydantic import BaseModel

from src.agents.agent import root_agent
from src.models.input import CountryInput

router = APIRouter()

session_service = InMemorySessionService()
runner = Runner(agent=root_agent, app_name="my_app", session_service=session_service)


class PromptRequest(BaseModel):
    prompt: str
    form: CountryInput


@router.post("/prompt", tags=["prompt"])
async def prompt(prompt_request: PromptRequest):
    """Send a prompt to the root agent and get a response."""
    # Create a new session
    session = await session_service.create_session(
        app_name="my_app",
        user_id="example_user",
        state={"key": "value"},
    )

    content = types.Content(role="user", parts=[types.Part(text=prompt_request.prompt)])

    async for event in runner.run_async(
        user_id=session.user_id, session_id=session.id, new_message=content
    ):
        if event.is_final_response():
            print(f"Agent Response: {event.content.parts[0].text}")
            return {"response": event.content.parts[0].text}
