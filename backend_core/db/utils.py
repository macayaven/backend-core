# backend_core/db/utils.py
"""Database utilities."""

from datetime import datetime, timezone
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.orm import Session

from backend_core.core.security import get_password_hash
from backend_core.db.base_class import Base
from backend_core.db.migrations import run_migrations
from backend_core.db.session import SessionLocal

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """Base class for CRUD operations."""

    def __init__(self, model: Type[ModelType]):
        """Initialize CRUD object with SQLAlchemy model."""
        self.model = model

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        """Get a record by ID."""
        return db.get(self.model, id)

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        """Get multiple records."""
        return db.query(self.model).offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        """Create a new record."""
        obj_in_data = jsonable_encoder(obj_in)
        if "password" in obj_in_data:
            # Convert password to hashed_password
            hashed_password = get_password_hash(obj_in_data.pop("password"))
            obj_in_data["hashed_password"] = hashed_password

        db_obj = self.model(**obj_in_data)  # type: ignore
        db_obj.created_at = datetime.now(timezone.utc)
        db_obj.updated_at = datetime.now(timezone.utc)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        """Update a record."""
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if "password" in update_data:
            hashed_password = get_password_hash(update_data.pop("password"))
            update_data["hashed_password"] = hashed_password

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db_obj.updated_at = datetime.now(timezone.utc)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int) -> ModelType:
        """Remove a record."""
        obj = db.get(self.model, id)
        if obj is None:
            raise Exception(f"No record found with id={id}")
        db.delete(obj)
        db.commit()
        return obj


def verify_database() -> bool:
    """
    Check if database connection is working and run migrations.

    Returns:
        bool: True if connection is successful and migrations run, False otherwise
    """
    try:
        db = SessionLocal()
        # Execute a simple query using SQLAlchemy text
        db.execute(text("SELECT 1"))
        # Run migrations
        run_migrations()
        return True
    except Exception as e:
        print(f"Database verification failed: {e}")
        return False
    finally:
        db.close()
