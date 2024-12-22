from fastapi import status
from fastapi.testclient import TestClient


def test_root_endpoint(client: TestClient) -> None:
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "message" in data
    assert "version" in data
    assert "docs_url" in data


def test_health_check(client: TestClient) -> None:
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "status" in data
    assert "database" in data
    assert "version" in data


def test_global_exception_handler(client: TestClient) -> None:
    """Test global exception handler."""
    # Force an error by sending invalid data
    response = client.post(
        "/api/v1/users/",
        json={"invalid": "json"},  # Use `json` to send a dictionary
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
