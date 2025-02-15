from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_main():
    """Prueba básica de que la API responde"""
    response = client.get("/api")
    assert response.status_code == 200
    assert "message" in response.json()

def test_health_check():
    """Prueba de endpoint de health check"""
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
