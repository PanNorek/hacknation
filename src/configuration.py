from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings


class Configuration(BaseSettings):
    # API Keys
    gemini_api_key: Optional[str] = Field(default=None, env="GEMINI_API_KEY")
    gemini_project_name: Optional[str] = Field(default=None, env="GEMINI_PROJECT_NAME")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
