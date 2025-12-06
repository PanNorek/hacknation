from typing import Optional, List
from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings


class DB(BaseSettings):
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_db: str = "hacknation"
    postgres_user: str = "postgres"
    postgres_password: str = ""

    # Important!
    model_config = {
        "env_prefix": "DB_",  # Only load env vars starting with POSTGRES_
        "extra": "ignore",  # Ignore unrelated env vars like GOOGLE_API_KEY
        "env_file": ".env",
        "case_sensitive": False,
    }


class Configuration(BaseSettings):
    # Gemini / Google API
    google_api_key: Optional[SecretStr] = Field(default=None)
    google_model_name: str = "gemini-2.0-flash"
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: int = Field(default=1000, gt=0)
    logfire_token: SecretStr = SecretStr("")

    # Server settings
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False
    reload: bool = False

    # CORS
    cors_origins: List[str] = ["*"]
    cors_allow_credentials: bool = True
    cors_allow_methods: List[str] = ["*"]
    cors_allow_headers: List[str] = ["*"]

    # Nested DB settings — SAFE!
    db: DB = DB()

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": False,
        "extra": "ignore",  # ignore unexpected env variables at top level too
    }
