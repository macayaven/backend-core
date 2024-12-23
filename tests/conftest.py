"""Test configuration and fixtures."""

from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from backend_core.core.config import settings
from backend_core.core.security import get_password_hash
from backend_core.db.base_class import Base
from backend_core.db.session import get_db
from backend_core.main import app
from backend_core.models.user import User


@pytest.fixture
def engine() -> Generator[Engine, None, None]:
    """Create engine for testing."""
    # Use the Docker PostgreSQL server for testing
    test_db_url = str(settings.DATABASE_URL)
    engine = create_engine(test_db_url)
    Base.metadata.create_all(bind=engine)
    yield engine


@pytest.fixture(autouse=True)
def db_session(engine: Engine) -> Generator[Session, None, None]:
    """Create a fresh database session for each test."""
    connection = engine.connect()
    transaction = connection.begin()
    Session = sessionmaker(bind=connection)
    session = Session()

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def client(db_session: Session) -> Generator[TestClient, None, None]:
    """Create FastAPI test client."""

    def override_get_db() -> Generator[Session, None, None]:
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def test_user(db_session: Session) -> User:
    """Create a test user."""
    user = User()
    user.email = "test@example.com"
    user.hashed_password = get_password_hash("password")  # Hash the password properly
    user.is_active = True
    user.is_superuser = False
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def token_headers(client: TestClient, test_user: User) -> dict[str, str]:
    """Get token headers for authenticated requests."""
    login_data = {
        "username": test_user.email,
        "password": "password",
    }
    response = client.post("/api/v1/auth/login", data=login_data)
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
