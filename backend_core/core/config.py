"""Configuration management for the application."""

from functools import lru_cache
from pathlib import Path
from typing import List, Optional, Union

from pydantic import AnyHttpUrl, Field, PostgresDsn, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    # API configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Backend Core"
    VERSION: str = "0.1.0"

    # Environment
    TARGET: str = "development"
    ENV_FILE: Optional[str] = None

    # Security
    SECRET_KEY: str = Field(..., alias="SECRET_KEY")
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
    POSTGRES_SERVER: str = Field(..., alias="POSTGRES_SERVER")
    POSTGRES_USER: str = Field(..., alias="POSTGRES_USER")
    POSTGRES_PASSWORD: str = Field(..., alias="POSTGRES_PASSWORD")
    POSTGRES_DB: str = Field(..., alias="POSTGRES_DB")
    POSTGRES_PORT: str = Field(..., alias="POSTGRES_PORT")

    @property
    def DATABASE_URL(self) -> str:
        """Get database URL."""
        return str(
            PostgresDsn.build(
                scheme="postgresql",
                username=self.POSTGRES_USER,
                password=self.POSTGRES_PASSWORD,
                host=self.POSTGRES_SERVER,
                port=int(self.POSTGRES_PORT),
                path=self.POSTGRES_DB,
            )
        )

    # First superuser
    FIRST_SUPERUSER: str = Field(..., alias="FIRST_SUPERUSER")
    FIRST_SUPERUSER_PASSWORD: str = Field(..., alias="FIRST_SUPERUSER_PASSWORD")

    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file=".env",
        extra="ignore",
        env_file_encoding="utf-8",
    )

    def update_env(self, target: str) -> None:
        """Update environment settings."""
        self.TARGET = target
        env_file = Path(f".env.{target}")
        if env_file.exists():
            self.ENV_FILE = str(env_file)
            self.model_config["env_file"] = str(env_file)
            self.model_validate({})


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()  # type: ignore[call-arg]


# Create a settings instance for import
settings = get_settings()
