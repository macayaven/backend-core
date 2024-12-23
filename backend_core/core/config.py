"""Configuration management for the application."""

from functools import lru_cache
from typing import List, Optional, Union

from pydantic import AnyHttpUrl, PostgresDsn, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    # API configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Backend Core"
    VERSION: str = "0.1.0"

    # Security
    SECRET_KEY: str = "development_secret_key"  # Default for development
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALGORITHM: str = "HS256"

    # CORS
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        """Validate CORS origins."""
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # PostgreSQL Database
    POSTGRES_SERVER: str = "localhost"  # Default for local development
    POSTGRES_USER: str = "postgres"  # Default for development
    POSTGRES_PASSWORD: str = "postgres"  # Default for development
    POSTGRES_DB: str = "app"  # Default for development
    POSTGRES_PORT: str = "5432"
    DOCKER_POSTGRES_SERVER: Optional[str] = None

    @property
    def DATABASE_URL(self) -> str:
        """Get database URL."""
        # Override POSTGRES_SERVER if running in Docker
        server = self.DOCKER_POSTGRES_SERVER or self.POSTGRES_SERVER

        return str(
            PostgresDsn.build(
                scheme="postgresql",
                username=self.POSTGRES_USER,
                password=self.POSTGRES_PASSWORD,
                host=server,
                port=int(self.POSTGRES_PORT),
                path=self.POSTGRES_DB,
            )
        )

    # First superuser
    FIRST_SUPERUSER_EMAIL: str = "admin@example.com"  # Default for development
    FIRST_SUPERUSER_PASSWORD: str = "admin"  # Default for development

    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file=".env.test" if __name__ == "tests.conftest" else ".env",
        extra="ignore",
        env_file_encoding="utf-8",
    )


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


# Create a settings instance for import
settings = get_settings()
