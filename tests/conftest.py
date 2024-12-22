from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from backend_core.core.config import settings
from backend_core.db.base_class import Base
from backend_core.db.session import get_db
from backend_core.main import app
from backend_core.models.user import User


@pytest.fixture(scope="session")
def engine() -> Generator[Engine, None, None]:
    """Create engine for testing."""
    engine = create_engine(settings.DATABASE_URL)  # Use PostgreSQL database URL
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
    app.dependency_overrides.clear()


@pytest.fixture
def test_user(db_session: Session) -> User:
    """Create a test user for each test that needs it."""
    import uuid

    from backend_core.core.security import get_password_hash
    from backend_core.models.user import User

    user = User()
    user.id = uuid.uuid4()
    user.email = f"test_{uuid.uuid4()}@example.com"
    user.hashed_password = get_password_hash("testpassword")
    user.first_name = "Test"
    user.last_name = "User"
    user.is_active = True

    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def token_headers(client: TestClient, test_user: User) -> dict[str, str]:
    """Get token headers for authenticated requests."""
    login_data = {"username": test_user.email, "password": "testpassword"}
    response = client.post(f"{settings.API_V1_STR}/auth/login", data=login_data)
    access_token = response.json()["access_token"]
    return {"Authorization": f"Bearer {access_token}"}
