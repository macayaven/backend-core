"""Application settings management."""

from functools import lru_cache
from typing import List

from pydantic import AnyHttpUrl, Field, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings managed as a singleton."""

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

    # API configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Backend Core"
    VERSION: str = "0.1.0"

    # Security
    SECRET_KEY: str = Field(..., alias="SECRET_KEY")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALGORITHM: str = "HS256"

    # CORS
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    # Database
    DATABASE_URL: PostgresDsn = Field(..., alias="DATABASE_URL")

    # Target environment
    TARGET: str = "development"


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


# Create singleton instance
settings = get_settings()
