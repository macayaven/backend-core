from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, MetaData, inspect
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.orm import Mapped, mapped_column


@as_declarative(metadata=MetaData())
class Base:
    """
    Base class for all SQLAlchemy models.

    This base provides:
    - Automatic __tablename__ generation unless overridden
    - Common columns (created_at, updated_at)
    - Common serialization methods
    """

    # SQLAlchemy requires this
    id: Mapped[Any]

    # Generate __tablename__ automatically using class name
    @declared_attr.directive
    @classmethod
    def __tablename__(cls) -> str:
        """
        Generates table name automatically from class name.
        Converts CamelCase to snake_case (e.g., UserModel -> user_model)
        """
        return cls.__name__.lower()

    # Common columns for all models
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    def dict(self) -> dict:
        """
        Convert model instance to dictionary.
        Useful for serialization.
        """
        inspection = inspect(self)
        if inspection is None:
            return {}
        if inspection.mapper is None:
            return {}
        return {column.key: getattr(self, column.key) for column in inspection.mapper.columns}

    def __repr__(self) -> str:
        """
        String representation of the model.
        Shows class name and id for easier debugging.
        """
        return f"<{self.__class__.__name__}(id={getattr(self, 'id', None)})>"
