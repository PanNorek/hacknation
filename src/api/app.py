import logging
import sys
from pprint import pprint

import logfire
from fastapi import FastAPI

from src.api.v1.routes import create_routes
from src.configuration import Configuration

config = Configuration()


def setup_logging():
    """Configure unified logging for FastAPI and uvicorn."""
    # Create formatter for consistent log format
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    # Remove any existing handlers to avoid duplication
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # Configure uvicorn loggers to use our format
    uvicorn_logger = logging.getLogger("uvicorn")
    uvicorn_logger.handlers.clear()  # Remove default handlers
    uvicorn_logger.setLevel(logging.INFO)
    uvicorn_logger.addHandler(console_handler)
    uvicorn_logger.propagate = False  # Don't propagate to root

    uvicorn_access_logger = logging.getLogger("uvicorn.access")
    uvicorn_access_logger.handlers.clear()
    uvicorn_access_logger.setLevel(logging.INFO)
    uvicorn_access_logger.addHandler(console_handler)
    uvicorn_access_logger.propagate = False

    # Configure fastapi logger
    fastapi_logger = logging.getLogger("fastapi")
    fastapi_logger.setLevel(logging.INFO)
    fastapi_logger.addHandler(console_handler)
    fastapi_logger.propagate = False

    # Create logger for this module
    logger = logging.getLogger(__name__)
    return logger


def create_app():
    # Setup logging first (only if not already configured)
    logger = setup_logging()

    logger.info("Initializing FastAPI application...")

    app = FastAPI(
        title="HackNation AI Agent API",
        description="An AI agent API powered by Google GenAI and FastAPI.",
        version="1.0.0",
    )

    # Configure logfire for application observability
    try:
        logfire.configure()
        logfire.instrument_pydantic_ai()
        logger.info("✅ Logfire observability enabled")
    except Exception as e:
        logger.warning(
            f"⚠️  Logfire configuration failed: {e}. Continuing without observability."
        )

    # Add startup event
    @app.on_event("startup")
    async def startup_event():
        logger.info("🚀 HackNation AI Agent API is starting up...")
        logger.info("📚 Loading routes and middleware...")
        logger.info(f"Configuration:")
        pprint(config.model_dump())

    # Add shutdown event
    @app.on_event("shutdown")
    async def shutdown_event():
        logger.info("🛑 HackNation AI Agent API is shutting down...")

    create_routes(app)

    logger.info("✅ FastAPI application created successfully")
    return app
