"""Test dependencies module."""

from datetime import datetime, timedelta, timezone
from typing import AsyncGenerator

import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient
from jose import jwt
from sqlalchemy.orm import Session

from backend_core.core.deps import decode_token, get_current_user, get_user_by_email
from backend_core.core.settings import settings
from backend_core.models.user import User


def test_decode_token() -> None:
    """Test decoding a valid token."""
    expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode = {"exp": expire, "sub": "test@example.com"}
    token = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    email = decode_token(token)
    assert email == "test@example.com"


def test_decode_token_invalid() -> None:
    """Test decoding an invalid token."""
    token = "invalid.token.payload"
    email = decode_token(token)
    assert email is None


def test_get_user_by_email(db_session: Session) -> None:
    """Test retrieving a user by email."""
    # Create a test user
    now = datetime.now(timezone.utc)
    user = User(
        email="test@example.com",
        hashed_password="hashed_password",
        is_superuser=False,
        created_at=now,
        updated_at=now,
    )
    db_session.add(user)
    db_session.commit()

    retrieved_user = get_user_by_email("test@example.com", db_session)
    assert retrieved_user is not None
    assert retrieved_user.email == "test@example.com"


def test_get_user_by_email_not_found(db_session: Session) -> None:
    """Test retrieving a non-existent user."""
    user = get_user_by_email("nonexistent@example.com", db_session)
    assert user is None


async def test_get_current_user_valid(client: TestClient, db_session: Session) -> None:
    """Test getting current user with a valid token."""
    # Create a test user
    now = datetime.now(timezone.utc)
    user = User(
        email="test@example.com",
        hashed_password="hashed_password",
        is_superuser=False,
        created_at=now,
        updated_at=now,
    )
    db_session.add(user)
    db_session.commit()

    # Create a valid token
    expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode = {"exp": expire, "sub": "test@example.com"}
    token = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    # Test getting current user
    current_user = await get_current_user(token, db_session)
    assert current_user is not None
    assert current_user.email == "test@example.com"


async def test_get_current_user_invalid_token(client: TestClient, db_session: Session) -> None:
    """Test getting current user with an invalid token."""
    with pytest.raises(HTTPException):
        await get_current_user("invalid.token", db_session)


async def test_get_current_user_user_not_found(client: TestClient, db_session: Session) -> None:
    """Test getting current user with a token for a non-existent user."""
    # Create a token for a non-existent user
    expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode = {"exp": expire, "sub": "nonexistent@example.com"}
    token = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    # Test getting current user
    with pytest.raises(HTTPException):
        await get_current_user(token, db_session)
