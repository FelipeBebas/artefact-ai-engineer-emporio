"""Testes automatizados para os endpoints REST da API FastAPI."""

from unittest.mock import patch
import pytest
from fastapi.testclient import TestClient
from src.app import api_app


@pytest.fixture
def client():
    """Fixture que provê um TestClient para a API FastAPI."""
    return TestClient(api_app)


def test_health_endpoint(client):
    """Garante que o endpoint de saúde responde 200 OK com metadados corretos."""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["version"] == "2.0.0"
    assert "Empório da Música" in data["service"]


def test_catalog_endpoint_with_filters(client):
    """Testa consulta de catálogo via API HTTP com filtros de categoria e preço."""
    response = client.get("/api/catalog?categoria=Violões&preco_max=1000")
    assert response.status_code == 200
    products = response.json()
    assert isinstance(products, list)
    assert len(products) > 0
    for p in products:
        assert p["price_brl"] <= 1000.0
        assert p["category_name"] == "Violões"


def test_catalog_endpoint_not_found(client):
    """Testa busca por termo inexistente retornando lista vazia."""
    response = client.get("/api/catalog?termo=instrumento_alienigena_xyz999")
    assert response.status_code == 200
    assert response.json() == []


def test_chat_endpoint(client):
    """Testa chamada POST /api/chat com mensagem e sessão persistida."""
    mock_reply = "Olá! Como posso ajudar seu som hoje?"

    with patch("src.app.run_agent_message", return_value=mock_reply):
        response = client.post(
            "/api/chat",
            json={"message": "Olá!", "session_id": "sess_test_999"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["response"] == mock_reply
        assert data["session_id"] == "sess_test_999"
