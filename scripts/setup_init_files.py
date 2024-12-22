# scripts/setup_init_files.py
from pathlib import Path

INIT_CONTENTS = {
    "backend_core/__init__.py": '''"""
Backend Core package.
Main package initialization.
"""

__version__ = "0.1.0"
''',
    "backend_core/api/__init__.py": '''"""API package for all versions."""
''',
    "backend_core/api/v1/__init__.py": '''"""API v1 package."""
''',
    "backend_core/api/v1/endpoints/__init__.py": '''"""API v1 endpoints."""
''',
    "backend_core/core/__init__.py": '''"""Core functionality package."""
''',
    "backend_core/db/__init__.py": '''"""Database package."""
''',
    "backend_core/models/__init__.py": '''"""SQLAlchemy models."""
from backend_core.models.user import User

__all__ = ["User"]
''',
    "backend_core/schemas/__init__.py": '''"""Pydantic schemas."""
from backend_core.schemas.user import UserCreate, UserRead

__all__ = ["UserCreate", "UserRead"]
''',
}


def create_init_files() -> None:
    """Create all __init__.py files with their contents."""
    root_dir = Path(__file__).parent.parent

    print("Creating __init__.py files...")

    for file_path, content in INIT_CONTENTS.items():
        # Create full path
        full_path = root_dir / file_path

        # Create directory if it doesn't exist
        full_path.parent.mkdir(parents=True, exist_ok=True)

        # Create file with content
        full_path.write_text(content)
        print(f"Created: {file_path}")


if __name__ == "__main__":
    create_init_files()
    print("\nAll __init__.py files have been created successfully!")
