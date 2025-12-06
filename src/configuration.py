from typing import List, Optional

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings


class Configuration(BaseSettings):
    # Legacy fields (optional for backwards compatibility)
    google_api_key: Optional[SecretStr] = Field(default=None, env="GOOGLE_API_KEY")
    google_model_name: str = Field(default="gemini-2.0-flash", env="GOOGLE_MODEL_NAME")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0, env="TEMPERATURE")
    max_tokens: int = Field(default=1000, gt=0, env="MAX_TOKENS")
    logfire_token: Optional[SecretStr] = Field(default=None, env="LOGFIRE_TOKEN")

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

    # API Keys - support both GEMINI_API_KEY and GOOGLE_API_KEY
    gemini_api_key: Optional[str] = Field(default=None, env="GEMINI_API_KEY")
    gemini_project_name: Optional[str] = Field(default=None, env="GEMINI_PROJECT_NAME")

    # Gemini Model Configuration
    gemini_model_name: str = Field(default="gemini-2.0-flash", env="GEMINI_MODEL_NAME")
    gemini_temperature: float = Field(default=0.2, env="GEMINI_TEMPERATURE")
    gemini_max_tokens: int = Field(default=4096, env="GEMINI_MAX_TOKENS")

    # Logging Configuration
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    log_dir: str = Field(default="logs", env="LOG_DIR")

    # Report Configuration
    report_dir: str = Field(default="reports", env="REPORT_DIR")
    report_page_size: str = Field(default="A4", env="REPORT_PAGE_SIZE")  # A4 or letter

    # Simulation Configuration
    max_other_countries_context: int = Field(
        default=5, env="MAX_OTHER_COUNTRIES_CONTEXT"
    )

    class Config:
        env_file = ".env"  # Automatically loads .env file from project root
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "ignore"  # Ignore extra fields from .env
