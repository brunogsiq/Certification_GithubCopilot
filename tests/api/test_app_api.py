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
    # Arrange
    # Nenhuma preparação necessária

    # Act
    response = client.get("/")

    # Assert
    assert response.status_code == 200 or response.status_code == 307
    # Aceita 307 (redirect) ou 200 (caso FastAPI trate diferente)

# Teste GET /activities
def test_get_activities():
    # Arrange
    # Nenhuma preparação necessária, pois o fixture já inicializa as atividades

    # Act
    response = client.get("/activities")
    data = response.json()

    # Assert
    assert response.status_code == 200
    assert "Python" in data
    assert "GitHub" in data

# Teste POST /activities/{activity_name}/signup
def test_signup_success():
    # Arrange
    activity = "Python"
    email = "user@example.com"
    url = f"/activities/{activity}/signup?email={email}"

    # Act
    response = client.post(url)

    # Assert
    assert response.status_code == 200
    assert "Inscrição realizada" in response.json()["message"]
    assert email in activities[activity]["participants"]

def test_signup_duplicate():
    # Arrange
    activity = "Python"
    email = "user@example.com"
    url = f"/activities/{activity}/signup?email={email}"
    client.post(url)

    # Act
    response = client.post(url)

    # Assert
    assert response.status_code == 400
    assert "já está inscrito" in response.json()["detail"]

def test_signup_activity_not_found():
    # Arrange
    activity = "Inexistente"
    email = "user@example.com"
    url = f"/activities/{activity}/signup?email={email}"

    # Act
    response = client.post(url)

    # Assert
    assert response.status_code == 404
    assert "não encontrada" in response.json()["detail"]

# Teste DELETE /activities/{activity_name}/signup
def test_remove_success():
    # Arrange
    activity = "GitHub"
    email = "user@example.com"
    url = f"/activities/{activity}/signup?email={email}"
    client.post(url)

    # Act
    response = client.delete(url)

    # Assert
    assert response.status_code == 200
    assert "removido com sucesso" in response.json()["message"]
    assert email not in activities[activity]["participants"]

def test_remove_not_signed_up():
    # Arrange
    activity = "GitHub"
    email = "user@example.com"
    url = f"/activities/{activity}/signup?email={email}"

    # Act
    response = client.delete(url)

    # Assert
    assert response.status_code == 400
    assert "não está inscrito" in response.json()["detail"]

def test_remove_activity_not_found():
    # Arrange
    activity = "Inexistente"
    email = "user@example.com"
    url = f"/activities/{activity}/signup?email={email}"

    # Act
    response = client.delete(url)

    # Assert
    assert response.status_code == 404
    assert "não encontrada" in response.json()["detail"]
