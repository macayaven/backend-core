"""Test configuration and fixtures."""

from typing import Generator

import psycopg2
import pytest
from fastapi.testclient import TestClient
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from backend_core.core.config import settings
from backend_core.core.security import get_password_hash
from backend_core.db.session import get_db
from backend_core.db.utils import verify_database
from backend_core.main import app
from backend_core.models.user import User

# Update settings to use test environment
settings.update_env("test")


def terminate_database_connections(dbname: str) -> None:
    """Terminate all connections to the database."""
    conn = psycopg2.connect(
        dbname="postgres",
        user=settings.POSTGRES_USER,
        password=settings.POSTGRES_PASSWORD,
        host=settings.POSTGRES_SERVER,
        port=settings.POSTGRES_PORT,
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()

    try:
        # Terminate all connections to the database
        cur.execute(
            f"""
            SELECT pg_terminate_backend(pg_stat_activity.pid)
            FROM pg_stat_activity
            WHERE pg_stat_activity.datname = '{dbname}'
            AND pid <> pg_backend_pid();
            """
        )
    finally:
        cur.close()
        conn.close()


@pytest.fixture(scope="session", autouse=True)
def setup_test_db() -> None:
    """Set up test database and run migrations."""
    # Store original database name
    original_db = settings.POSTGRES_DB

    # Terminate existing connections to the test database
    terminate_database_connections(original_db)

    # Connect to default postgres database to create/drop test database
    temp_db_url = str(settings.DATABASE_URL).replace(original_db, "postgres")
    engine = create_engine(temp_db_url)

    with engine.connect() as conn:
        conn.execute(text("COMMIT"))  # Close any open transactions
        conn.execute(text(f"DROP DATABASE IF EXISTS {original_db}"))
        conn.execute(text(f"CREATE DATABASE {original_db}"))

    # Run migrations on test database
    verify_database()


@pytest.fixture
def engine() -> Generator[Engine, None, None]:
    """Create engine for testing."""
    test_db_url = str(settings.DATABASE_URL)
    engine = create_engine(test_db_url)
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
