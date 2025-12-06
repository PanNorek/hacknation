import uuid
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, Query
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from pydantic import BaseModel

from src.agents.agent import root_agent
from src.models.input import CountryInput
from src.models.prompts import PromptRequest, SystemInstructionInput

router = APIRouter()

APP_NAME = "root_agent_app"

session_service = InMemorySessionService()
runner = Runner(agent=root_agent, app_name=APP_NAME, session_service=session_service)

# Store user sessions and contexts
user_sessions = {}


class PredictionRequest(BaseModel):
    prompt: str
    form: CountryInput


async def get_runner() -> Runner:
    """FastAPI dependency to get the runner instance."""
    return runner


async def get_user_session(
    user_id: Annotated[Optional[str], Query(description="User ID")] = None,
) -> tuple[str, dict]:
    """FastAPI dependency to get or create user session."""
    if user_id is None:
        user_id = f"user_{uuid.uuid4().hex[:8]}"

    if user_id not in user_sessions:
        # Create a new session for this user
        session = await session_service.create_session(
            app_name=APP_NAME,
            user_id=user_id,
        )
        user_sessions[user_id] = {"session": session}

    return user_id, user_sessions[user_id]


UserSessionDep = Annotated[tuple[str, dict], Depends(get_user_session)]
RunnerDep = Annotated[Runner, Depends(get_runner)]


@router.post("/prompt", tags=["prompt"])
async def prompt(
    prompt_request: PromptRequest,
    user_session: UserSessionDep,
    agent_runner: RunnerDep,
):
    """Send a prompt to the root agent and get a response."""
    try:
        user_id, user_data = user_session
        session = user_data["session"]

        # Create message content
        content = types.Content(
            role="user", parts=[types.Part(text=prompt_request.prompt)]
        )

        # Run the agent and collect response
        final_response = None
        async for event in agent_runner.run_async(
            user_id=session.user_id, session_id=session.id, new_message=content
        ):
            if event.is_final_response():
                final_response = event.content.parts[0].text
                print(f"Agent Response: {final_response}")
                break

        return {
            "response": final_response,
            "user_id": user_id,
            "session_id": session.id,
            "success": True,
        }
    except Exception as e:
        print(f"Error running agent: {str(e)}")
        import traceback

        traceback.print_exc()
        return {
            "response": f"Error: {str(e)}",
            "success": False,
            "error": True,
        }


@router.post("/prediction", tags=["prompt"])
async def prediction(
    prediction_request: PredictionRequest,
    user_session: UserSessionDep,
    agent_runner: RunnerDep,
):
    """Send a prompt with country data to the root agent and get a prediction."""
    try:
        user_id, user_data = user_session
        session = user_data["session"]

        # Combine prompt with form data
        full_prompt = f"{prediction_request.prompt}\n\nCountry Data:\n{prediction_request.form.model_dump_json(indent=2)}"

        content = types.Content(role="user", parts=[types.Part(text=full_prompt)])

        # Run the agent and collect response
        final_response = None
        async for event in agent_runner.run_async(
            user_id=session.user_id, session_id=session.id, new_message=content
        ):
            if event.is_final_response():
                print(f"Agent Response: {event.content}")
                final_response = event.content.parts[0].text
                break

        return {
            "response": final_response,
            "user_id": user_id,
            "session_id": session.id,
            "success": True,
        }
    except Exception as e:
        print(f"Error running agent: {str(e)}")
        import traceback

        traceback.print_exc()
        return {
            "response": f"Error: {str(e)}",
            "success": False,
            "error": True,
        }


# @router.get("/instruction", tags=["agent"])
# async def instruction(user_session: UserSessionDep):
#     """Return system instructions for all known user sessions."""
#     user_id, _ = user_session
#     instruction = user_sessions[user_id]["system_instruction"]

#     return {
#         "instruction": instruction,
#     }
