from typing import List, Optional

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings


class Configuration(BaseSettings):
    google_api_key: SecretStr = Field(default=None, env="GOOGLE_API_KEY")
    google_model_name: str = Field(default="gemini-2.0-flash", env="GOOGLE_MODEL_NAME")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0, env="TEMPERATURE")
    max_tokens: int = Field(default=1000, gt=0, env="MAX_TOKENS")
    logfire_token: SecretStr = Field(default=SecretStr(""), env="LOGFIRE_TOKEN")

    # Server settings
    host: str = Field(default="0.0.0.0", env="HOST")
    port: int = Field(default=8000, env="PORT")
    debug: bool = Field(default=False, env="DEBUG")
    reload: bool = Field(default=False, env="RELOAD")

    # CORS settings
    cors_origins: List[str] = Field(default=["*"], env="CORS_ORIGINS")
    cors_allow_credentials: bool = Field(default=True, env="CORS_ALLOW_CREDENTIALS")
    cors_allow_methods: List[str] = Field(default=["*"], env="CORS_ALLOW_METHODS")
    cors_allow_headers: List[str] = Field(default=["*"], env="CORS_ALLOW_HEADERS")

    class Config:
        env_file = ".env"  # Automatically loads .env file from project root
        env_file_encoding = "utf-8"
        case_sensitive = False  # Environment variable names are case-insensitive
