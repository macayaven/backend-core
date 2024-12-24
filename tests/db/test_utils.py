from uuid import uuid4

from sqlalchemy.orm import Session

from backend_core.core.security import get_password_hash, verify_password
from backend_core.db.utils import CRUDBase
from backend_core.models.user import User
from backend_core.schemas.user import UserCreate, UserUpdate
from datetime import datetime, timezone


class TestCRUDBase:
    """Test CRUD base operations."""

    def test_get(self, db_session: Session) -> None:
        """Test getting a single record."""
        crud = CRUDBase[User, UserCreate, UserUpdate](User)

        # Create a user by setting attributes directly
        now = datetime.now(timezone.utc)
        user = User()
        user.id = uuid4()
        user.email = "get_test@example.com"
        user.hashed_password = get_password_hash("testpass")
        user.first_name = "Test"
        user.last_name = "User"
        user.created_at = now
        user.updated_at = now

        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

        db_user = crud.get(db_session, id=user.id)
        assert db_user is not None, "User should not be None"
        assert db_user.id == user.id
        assert db_user.email == user.email

    def test_get_multi(self, db_session: Session) -> None:
        """Test getting multiple records."""
        crud = CRUDBase[User, UserCreate, UserUpdate](User)

        # Create multiple users
        now = datetime.now(timezone.utc)
        users = []
        for i in range(3):
            user = User()
            user.id = uuid4()
            user.email = f"multi_test{i}@example.com"
            user.hashed_password = get_password_hash("testpass")
            user.first_name = f"Test{i}"
            user.last_name = "User"
            user.created_at = now
            user.updated_at = now
            users.append(user)
            db_session.add(user)

        db_session.commit()

        db_users = crud.get_multi(db_session, skip=0, limit=2)
        assert len(db_users) == 2

    def test_create(self, db_session: Session) -> None:
        """Test creating a record."""
        crud = CRUDBase[User, UserCreate, UserUpdate](User)
        email = f"create_test_{uuid4()}@example.com"
        user_in = UserCreate(
            email=email,
            password="testpass",  # This will be converted to hashed_password
            first_name="Test",
            last_name="User",
        )

        user = crud.create(db_session, obj_in=user_in)
        db_session.refresh(user)

        assert user.email == email
        assert user.first_name == "Test"
        assert hasattr(user, "hashed_password")
        assert not hasattr(user, "password")
        assert verify_password("testpass", user.hashed_password)
        assert user.created_at is not None
        assert user.updated_at is not None

    def test_update(self, db_session: Session) -> None:
        """Test updating a record."""
        crud = CRUDBase[User, UserCreate, UserUpdate](User)

        # Create initial user
        now = datetime.now(timezone.utc)
        user = User()
        user.id = uuid4()
        user.email = f"update_test_{uuid4()}@example.com"
        user.hashed_password = get_password_hash("testpass")
        user.first_name = "Test"
        user.last_name = "User"
        user.created_at = now
        user.updated_at = now

        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

        # Update user
        user_update = UserUpdate(first_name="Updated")
        updated_user = crud.update(db_session, db_obj=user, obj_in=user_update)
        db_session.refresh(updated_user)

        # Fetch fresh instance from database
        fresh_user = crud.get(db_session, id=user.id)
        assert fresh_user is not None, "User should not be None"
        assert fresh_user.first_name == "Updated"

    def test_update_with_dict(self, db_session: Session) -> None:
        """Test updating a record with dict."""
        crud = CRUDBase[User, UserCreate, UserUpdate](User)

        # Create initial user
        now = datetime.now(timezone.utc)
        user = User()
        user.id = uuid4()
        user.email = f"update_dict_test_{uuid4()}@example.com"
        user.hashed_password = get_password_hash("testpass")
        user.first_name = "Test"
        user.last_name = "User"
        user.created_at = now
        user.updated_at = now

        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

        # Update using dict
        update_data = {"first_name": "Updated"}
        crud.update(db_session, db_obj=user, obj_in=update_data)

        # Fetch fresh instance from database
        fresh_user = crud.get(db_session, id=user.id)
        assert fresh_user is not None, "User should not be None"
        assert fresh_user.first_name == "Updated"

    def test_remove(self, db_session: Session) -> None:
        """Test removing a record."""
        crud = CRUDBase[User, UserCreate, UserUpdate](User)

        # Create initial user
        now = datetime.now(timezone.utc)
        user = User()
        user.id = uuid4()
        user.email = f"remove_test_{uuid4()}@example.com"
        user.hashed_password = get_password_hash("testpass")
        user.created_at = now
        user.updated_at = now

        db_session.add(user)
        db_session.commit()

        # Remove the user
        crud.remove(db_session, id=user.id)
        assert crud.get(db_session, id=user.id) is None
