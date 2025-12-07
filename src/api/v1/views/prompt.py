import os
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

# Limit AFC (Agent Function Calling) to prevent excessive tool usage
os.environ["GOOGLE_ADK_AFC_MAX_REMOTE_CALLS"] = "3"
os.environ["GOOGLE_ADK_MAX_TOOL_CALLS"] = "3"
os.environ["GOOGLE_ADK_MAX_FUNCTION_CALLS"] = "3"

# Additional safeguards for function calling limits
os.environ["MAX_TOOL_CALLS_PER_TURN"] = "2"
os.environ["MAX_FUNCTION_CALLS"] = "3"
os.environ["TOOL_CALL_LIMIT"] = "3"

router = APIRouter()

APP_NAME = "root_agent_app"

session_service = InMemorySessionService()
runner = Runner(agent=root_agent, app_name=APP_NAME, session_service=session_service)

# Store user sessions and contexts
user_sessions = {}


class PredictionRequest(BaseModel):
    prompt: str


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
        tools_used = []
        agent_tools_info = []
        tool_call_count = 0
        max_tool_calls = 3  # Additional runtime limit

        async for event in agent_runner.run_async(
            user_id=session.user_id, session_id=session.id, new_message=content
        ):
            # Collect tool usage information from various possible sources
            if hasattr(event, "tool_calls") and event.tool_calls:
                for tool_call in event.tool_calls:
                    tool_call_count += 1
                    if tool_call_count > max_tool_calls:
                        print(
                            f"⚠️ Tool call limit ({max_tool_calls}) exceeded, skipping additional calls"
                        )
                        break
                    tools_used.append(
                        {
                            "tool_name": getattr(tool_call, "name", "unknown"),
                            "parameters": getattr(tool_call, "arguments", {}),
                            "timestamp": getattr(event, "timestamp", None),
                        }
                    )

            # Check for tool results or tool usage in the event
            if hasattr(event, "tool_results") and event.tool_results:
                for tool_result in event.tool_results:
                    tools_used.append(
                        {
                            "tool_name": getattr(tool_result, "name", "unknown"),
                            "result": getattr(tool_result, "result", None),
                            "timestamp": getattr(event, "timestamp", None),
                        }
                    )

            if event.is_final_response():
                # Extract text content with error handling
                final_response = None
                try:
                    if hasattr(event, "content") and event.content:
                        if hasattr(event.content, "parts") and event.content.parts:
                            # Try to get text from parts
                            part = event.content.parts[0]
                            if hasattr(part, "text"):
                                final_response = part.text
                            elif hasattr(part, "content"):
                                final_response = str(part.content)
                            else:
                                final_response = str(part)
                        elif hasattr(event.content, "text"):
                            final_response = event.content.text
                        else:
                            final_response = str(event.content)
                    elif hasattr(event, "text"):
                        final_response = event.text
                    elif hasattr(event, "message"):
                        final_response = event.message
                    else:
                        final_response = str(event)
                except Exception as e:
                    print(f"Error extracting response text: {e}")
                    final_response = f"Error extracting response: {str(e)}"

                print(f"Agent Response: {final_response}")

                # Extract tools information from various possible locations
                if hasattr(event, "tools") and event.tools:
                    agent_tools_info = event.tools
                elif hasattr(event.content, "tools") and getattr(
                    event.content, "tools", None
                ):
                    agent_tools_info = event.content.tools
                elif hasattr(event, "tool_calls") and event.tool_calls:
                    # Convert tool calls to tools info
                    agent_tools_info = [
                        {
                            "name": getattr(tc, "name", "unknown"),
                            "args": getattr(tc, "arguments", {}),
                        }
                        for tc in event.tool_calls
                    ]

                break

        # Also try to get tools from the agent configuration
        agent_declared_tools = []
        if hasattr(root_agent, "tools") and root_agent.tools:
            agent_declared_tools = [
                {
                    "name": getattr(tool, "name", str(tool)),
                    "description": getattr(tool, "description", ""),
                }
                for tool in root_agent.tools
            ]

        return {
            "response": final_response,
            "tools": agent_tools_info if agent_tools_info else agent_declared_tools,
            "tools_used": tools_used,
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
