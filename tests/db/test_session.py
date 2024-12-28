from datetime import datetime, timezone
from uuid import uuid4

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from backend_core.core.security import get_password_hash
from backend_core.db.session import get_db
from backend_core.db.utils import verify_database
from backend_core.models.user import User


def test_get_db() -> None:
    """Test database session generator."""
    db_gen = get_db()
    db = next(db_gen)
    assert isinstance(db, Session)

    try:
        next(db_gen)  # Should raise StopIteration
    except StopIteration:
        pass  # This is expected


def test_db_session_context(client: "TestClient", db_session: Session) -> None:
    """Test database session context management."""
    # Create a test user by assigning attributes directly
    now = datetime.now(timezone.utc)
    test_user = User()
    test_user.id = uuid4()
    test_user.email = "session_test@example.com"
    test_user.hashed_password = get_password_hash("testpass")
    test_user.created_at = now
    test_user.updated_at = now

    db_session.add(test_user)
    db_session.commit()

    # Test that we can query the database
    queried_user = db_session.query(User).filter_by(email="session_test@example.com").first()
    assert queried_user is not None, "Queried user should not be None"
    assert queried_user.email == "session_test@example.com"


def test_database_connection() -> None:
    """Test database connection."""
    assert verify_database() is True
