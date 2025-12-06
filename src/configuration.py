from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional


class Configuration(BaseSettings):
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
    max_other_countries_context: int = Field(default=5, env="MAX_OTHER_COUNTRIES_CONTEXT")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "ignore"  # Ignore extra fields from .env
