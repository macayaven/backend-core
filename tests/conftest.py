"""Test configuration and fixtures."""

from datetime import datetime, timedelta, timezone
from typing import Generator
import time

import psycopg2
import pytest
from fastapi.testclient import TestClient
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from backend_core.core.security import get_password_hash
from backend_core.core.settings import get_settings, settings
from backend_core.db.session import get_db
from backend_core.db.migrations import run_migrations
from backend_core.main import app
from backend_core.models.user import User


def wait_for_database(max_retries: int = 30, retry_interval: float = 1.0) -> None:
    """Wait for the database to be ready."""
    retries = 0
    while retries < max_retries:
        try:
            conn = psycopg2.connect(
                dbname="postgres",
                user=settings.POSTGRES_USER,
                password=settings.POSTGRES_PASSWORD,
                host=settings.POSTGRES_SERVER,
                port=settings.POSTGRES_PORT,
            )
            conn.close()
            return
        except psycopg2.OperationalError:
            retries += 1
            time.sleep(retry_interval)
    
    raise Exception(f"Database not ready after {max_retries} retries")


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
    # Wait for the database to be ready
    wait_for_database()

    # Connect to postgres database to create/drop test database
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
        # Drop test database if it exists
        terminate_database_connections(settings.POSTGRES_DB)
        cur.execute(f"DROP DATABASE IF EXISTS {settings.POSTGRES_DB}")
        # Create test database
        cur.execute(f"CREATE DATABASE {settings.POSTGRES_DB}")
    finally:
        cur.close()
        conn.close()

    # Run migrations on test database
    run_migrations()


@pytest.fixture(scope="session")
def engine() -> Engine:
    """Create database engine for testing."""
    return create_engine(settings.DATABASE_URL, pool_pre_ping=True)


@pytest.fixture
def db_session(engine: Engine) -> Generator[Session, None, None]:
    """Create a fresh database session for each test."""
    connection = engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def client(db_session: Session) -> Generator[TestClient, None, None]:
    """Create FastAPI test client."""
    def override_get_db() -> Generator[Session, None, None]:
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def test_user(db_session: Session) -> User:
    """Create a test user."""
    now = datetime.now(timezone.utc)
    user = User(
        email="test@example.com",
        hashed_password=get_password_hash("password"),
        is_superuser=False,
        created_at=now,
        updated_at=now,
    )
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
    response = client.post(f"{settings.API_V1_STR}/auth/login", data=login_data)
    tokens = response.json()
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}
    return headers
