import pytest
from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)

@pytest.fixture(autouse=True)
def reset_activities():
    activities.clear()
    activities.update({
        "Python": {"participants": []},
        "GitHub": {"participants": []}
    })
    yield
    activities.clear()

# Teste GET /
def test_root_redirect():
    response = client.get("/")
    assert response.status_code == 200 or response.status_code == 307
    # Aceita 307 (redirect) ou 200 (caso FastAPI trate diferente)

# Teste GET /activities
def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Python" in data
    assert "GitHub" in data

# Teste POST /activities/{activity_name}/signup
def test_signup_success():
    response = client.post("/activities/Python/signup?email=user@example.com")
    assert response.status_code == 200
    assert "Inscrição realizada" in response.json()["message"]
    assert "user@example.com" in activities["Python"]["participants"]

def test_signup_duplicate():
    client.post("/activities/Python/signup?email=user@example.com")
    response = client.post("/activities/Python/signup?email=user@example.com")
    assert response.status_code == 400
    assert "já está inscrito" in response.json()["detail"]

def test_signup_activity_not_found():
    response = client.post("/activities/Inexistente/signup?email=user@example.com")
    assert response.status_code == 404
    assert "não encontrada" in response.json()["detail"]

# Teste DELETE /activities/{activity_name}/signup
def test_remove_success():
    client.post("/activities/GitHub/signup?email=user@example.com")
    response = client.delete("/activities/GitHub/signup?email=user@example.com")
    assert response.status_code == 200
    assert "removido com sucesso" in response.json()["message"]
    assert "user@example.com" not in activities["GitHub"]["participants"]

def test_remove_not_signed_up():
    response = client.delete("/activities/GitHub/signup?email=user@example.com")
    assert response.status_code == 400
    assert "não está inscrito" in response.json()["detail"]

def test_remove_activity_not_found():
    response = client.delete("/activities/Inexistente/signup?email=user@example.com")
    assert response.status_code == 404
    assert "não encontrada" in response.json()["detail"]
