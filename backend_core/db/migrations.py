"""Database migration utilities."""

from pathlib import Path

from alembic import command
from alembic.config import Config
from backend_core.core.settings import settings


def get_alembic_config() -> Config:
    """Get Alembic configuration."""
    # Get the directory where this file is located
    current_dir = Path(__file__).resolve().parent
    # Go up two levels to get to the backend_core directory
    backend_core_dir = current_dir.parent.parent
    # Create Alembic configuration
    alembic_cfg = Config(str(backend_core_dir / "alembic.ini"))
    # Set the script location to the migrations directory
    alembic_cfg.set_main_option("script_location", str(backend_core_dir / "alembic"))
    # Set the sqlalchemy.url
    alembic_cfg.set_main_option(
        "sqlalchemy.url",
        f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}"
        f"@{settings.POSTGRES_SERVER}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}",
    )
    return alembic_cfg


def run_migrations() -> None:
    """Run database migrations."""
    alembic_cfg = get_alembic_config()
    command.upgrade(alembic_cfg, "head")


def downgrade_migrations() -> None:
    """Downgrade database migrations."""
    alembic_cfg = get_alembic_config()
    command.downgrade(alembic_cfg, "base")
