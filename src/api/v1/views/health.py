from fastapi import APIRouter

router = APIRouter()


@router.get("/health", tags=["health"])
async def health():
    return {
        "message": "Welcome to HackNation AI Agent API",
        "version": "1.0.0",
        "endpoints": {
            "/prompt": "POST - Send prompts to the AI agent",
            "/agent_info": "GET - Get information about the AI agent",
        },
    }
