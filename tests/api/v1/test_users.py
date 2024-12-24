# tests/api/v1/test_users.py
from datetime import datetime
from datetime import timezone as tz
from typing import Any

from fastapi import status
from fastapi.testclient import TestClient

from backend_core.core.settings import settings
from backend_core.models.user import User


def test_create_user(client: TestClient) -> None:
    """Test user creation."""
    user_data = {
        "email": "new@example.com",
        "password": "newpassword123",
        "first_name": "New",
        "last_name": "User"
    }
    response = client.post(f"{settings.API_V1_STR}/users/", json=user_data)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["email"] == user_data["email"]
    assert "id" in data
    assert "password" not in data


def test_create_user_existing_email(client: TestClient, test_user: User) -> None:
    """Test creating user with existing email."""
    user_data = {
        "email": test_user.email,  # Using existing email
        "password": "anotherpassword",
        "first_name": "Another",
        "last_name": "User",
    }
    response = client.post(f"{settings.API_V1_STR}/users/", json=user_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_read_current_user(client: TestClient, test_user: User, token_headers: dict[str, str]) -> None:
    """Test reading current user data."""
    response = client.get(f"{settings.API_V1_STR}/users/me", headers=token_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["email"] == test_user.email
    assert "password" not in data
    assert data["first_name"] == test_user.first_name
    assert data["last_name"] == test_user.last_name


def test_update_current_user(client: TestClient, token_headers: dict[str, str]) -> None:
    """Test updating current user."""
    update_data = {"first_name": "Updated", "last_name": "Name"}
    response = client.put(f"{settings.API_V1_STR}/users/me", headers=token_headers, json=update_data)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["first_name"] == update_data["first_name"]
    assert data["last_name"] == update_data["last_name"]


def test_read_user_unauthorized(client: TestClient) -> None:
    """Test reading current user without authentication."""
    response = client.get(f"{settings.API_V1_STR}/users/me")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
