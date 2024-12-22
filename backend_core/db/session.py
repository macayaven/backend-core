# backend_core/db/session.py
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend_core.core.config import settings

# Create database engine
engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True, pool_size=5, max_overflow=10)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator:
    """
    Dependency function to get a database session.

    Yields:
        Session: SQLAlchemy session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
