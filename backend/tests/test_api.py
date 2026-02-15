import pytest
from fastapi.testclient import TestClient
from api_gateway.main import app

client = TestClient(app)

def test_health_endpoint():
    """Test that the health endpoint returns ok"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_root_endpoint():
    """Test that the root endpoint returns version info"""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()
    assert "Customer Database API" in response.json()["message"]

def test_unauthorized_access():
    """Test that protected endpoints require authentication"""
    response = client.get("/api/v1/workspaces")
    assert response.status_code == 403 or response.status_code == 401
