from fastapi.testclient import TestClient
from main import app
from unittest.mock import patch, AsyncMock
import pytest

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to TJSP Criminal Records API. Use /search to check records."}

def test_get_status():
    response = client.get("/status")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "online"
    assert "total_requests_processed" in data

@patch("main.search_tjsp", new_callable=AsyncMock)
def test_search_records_success(mock_search):
    # Arrange
    cpf = "123.456.789-00"
    mock_search.return_value = {
        "count": 1,
        "details": [{
            "number": "0000000-00.2023.8.26.0000",
            "degree": "1º Grau",
            "link": "http://test.com",
            "classe": "Execução Penal",
            "area": "Criminal",
            "assunto": "Pena Privativa de Liberdade",
            "data_distribuicao": "01/01/2023",
            "juiz": "Juiz Teste",
            "valor_acao": "R$ 1.000,00",
            "partes": ["Autor: Justiça Pública", "Réu: Fulano de Tal"],
            "movimentacoes": ["01/01/2023 - Processo distribuído"]
        }],
        "names": ["Fulano de Tal"]
    }
    
    # Act
    response = client.post("/search", json={"document": cpf})
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["document"] == cpf
    assert data["records_count"] == 1
    assert data["status"] == "success"
    assert len(data["processes"]) == 1
    assert data["processes"][0]["number"] == "0000000-00.2023.8.26.0000"
    assert "Fulano de Tal" in data["names"]

@patch("main.search_tjsp", new_callable=AsyncMock)
def test_search_records_not_found(mock_search):
    # Arrange
    cpf = "000.000.000-00"
    mock_search.return_value = {
        "count": 0,
        "details": [],
        "names": []
    }
    
    # Act
    response = client.post("/search", json={"document": cpf})
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["records_count"] == 0
    assert data["status"] == "success"
    assert data["processes"] == []

@patch("main.search_tjsp", new_callable=AsyncMock)
def test_search_records_error(mock_search):
    # Arrange
    mock_search.return_value = {"error": "Timeout error"}
    
    # Act
    response = client.post("/search", json={"document": "123.456.789-00"})
    
    # Assert
    assert response.status_code == 500
    assert "Search failed" in response.json()["detail"]

def test_search_missing_document():
    response = client.post("/search", json={})
    assert response.status_code == 422  # Validation error

def test_formatting_logic():
    # Test plain input gets formatted in response
    # We don't need to mock here because we are testing the formatting logic in the endpoint
    # but the endpoint calls search_tjsp, so we SHOULD mock it to avoid real calls
    with patch("main.search_tjsp", new_callable=AsyncMock) as mock_search:
        mock_search.return_value = {"count": 0, "details": [], "names": []}
        
        plain_cpf = "12345678900"
        formatted_cpf = "123.456.789-00"
        
        response = client.post("/search", json={"document": plain_cpf})
        
        assert response.status_code == 200
        assert response.json()["document"] == formatted_cpf
