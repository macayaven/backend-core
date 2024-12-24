"""Application settings management."""

from functools import lru_cache
from pathlib import Path
from typing import List, Union

from pydantic import AnyHttpUrl, Field, PostgresDsn, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings managed as a singleton."""

    # API configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Backend Core"
    VERSION: str = "0.1.0"

    # Environment
    TARGET: str = "development"

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
    POSTGRES_SERVER: str = Field(default="localhost", alias="POSTGRES_SERVER")
    POSTGRES_USER: str = Field(default="postgres", alias="POSTGRES_USER")
    POSTGRES_PASSWORD: str = Field(default="postgres", alias="POSTGRES_PASSWORD")
    POSTGRES_DB: str = Field(default="test_db", alias="POSTGRES_DB")
    POSTGRES_PORT: str = Field(default="5432", alias="POSTGRES_PORT")

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
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()  # type: ignore[call-arg]


# Create singleton instance
settings = get_settings()
