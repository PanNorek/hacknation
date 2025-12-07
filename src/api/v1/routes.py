from fastapi import APIRouter, FastAPI

from src.api.v1.views.agent_info import router as agent_info_router
from src.api.v1.views.health import router as health_router
from src.api.v1.views.prompt import router as prompt_router
from src.api.v1.views.instructions import router as instructions_router


def create_routes(app: FastAPI):
    app.include_router(health_router)
    app.include_router(agent_info_router)
    app.include_router(prompt_router)
    app.include_router(instructions_router)
