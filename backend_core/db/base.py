# backend_core/db/base.py
# Import all models here for Alembic
from backend_core.db.base_class import Base  # noqa
from backend_core.db.session import engine  # noqa
from backend_core.models.user import User  # noqa
