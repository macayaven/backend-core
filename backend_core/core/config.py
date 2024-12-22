# backend_core/core/config.py
from typing import List

from pydantic_settings import BaseSettings, SettingsError


class Settings(BaseSettings):
    # API configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Backend Core"
    VERSION: str = "0.1.0"

    # Security
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALGORITHM: str = "HS256"

    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]

    # PostgreSQL Database
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: str = "5432"

    # First superuser
    FIRST_SUPERUSER_EMAIL: str
    FIRST_SUPERUSER_PASSWORD: str

    # Environment
    ENVIRONMENT: str = "development"  # Default to production if not set

    @property
    def DATABASE_URL(self) -> str:
        """Construct database URL from settings."""
        return (
            f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    class Config:
        case_sensitive = True
        env_file = ".env"


# Create settings instance

try:
    settings = Settings()  # type: ignore
except SettingsError as e:
    print(f"Settings error: {e}")
