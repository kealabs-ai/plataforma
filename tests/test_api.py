import pytest
from fastapi.testclient import TestClient
import sys
import os
import json

# Adiciona o diretório raiz ao path para importações relativas
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.main import app

client = TestClient(app)

def test_status():
    """Testa se a rota de status está funcionando."""
    response = client.get("/status")
    assert response.status_code == 200
    assert response.json()["status"] == "online"

def test_unauthorized_access():
    """Testa se rotas protegidas requerem autenticação."""
    response = client.get("/users/me")
    assert response.status_code == 401

def test_invalid_login():
    """Testa se login com credenciais inválidas falha."""
    response = client.post(
        "/token",
        data={"username": "invalid_user", "password": "invalid_password"}
    )
    assert response.status_code == 401

# Mais testes seriam adicionados aqui para cobrir outras funcionalidades da API