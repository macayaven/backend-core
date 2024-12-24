# backend_core/db/base_class.py
"""Base model class."""

from datetime import datetime, timezone as tz
from typing import Any

from sqlalchemy import MetaData, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql import func

class Base(DeclarativeBase):
    """Base class for all database models."""

    metadata = MetaData()

    id: Any
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())

    def __init__(self, **kwargs: Any) -> None:
        """Initialize the base model."""
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.updated_at = datetime.now(tz.utc)

    def dict(self) -> dict[str, Any]:
        """Convert model to dictionary."""
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}

    def __repr__(self) -> str:
        """
        String representation of the model.
        Shows class name and id for easier debugging.
        """
        return f"<{self.__class__.__name__}(id={getattr(self, 'id', None)})>"
