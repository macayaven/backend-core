# tests/api/v1/test_auth.py
from fastapi import status
from fastapi.testclient import TestClient

from backend_core.core.settings import settings
from backend_core.models.user import User


def test_login_success(client: TestClient, test_user: User) -> None:
    """Test successful login."""
    login_data = {"username": test_user.email, "password": "password"}  # Changed from testpassword to password
    response = client.post(
        f"{settings.API_V1_STR}/auth/login", data=login_data  # Note: using data instead of json for form data
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client: TestClient, test_user: User) -> None:
    """Test login with wrong password."""
    login_data = {"username": test_user.email, "password": "wrongpassword"}
    response = client.post(f"{settings.API_V1_STR}/auth/login", data=login_data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_login_wrong_email(client: TestClient) -> None:
    """Test login with non-existent email."""
    login_data = {"username": "nonexistent@example.com", "password": "testpassword"}
    response = client.post(f"{settings.API_V1_STR}/auth/login", data=login_data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_token_validation(client: TestClient, token_headers: dict[str, str]) -> None:
    """Test token validation with protected endpoint."""
    response = client.get(f"{settings.API_V1_STR}/users/me", headers=token_headers)
    assert response.status_code == status.HTTP_200_OK
