import pytest
from src import app

# Mock de dados para testes
@pytest.fixture(autouse=True)
def reset_activities(monkeypatch):
    # Garante que o dicionário de atividades seja limpo antes de cada teste
    app.activities.clear()
    app.activities.update({
        "Python": {"participants": []},
        "GitHub": {"participants": []}
    })
    yield
    app.activities.clear()

# Testes para signup_for_activity
class TestSignupForActivity:
    def test_signup_success(self):
        # Arrange
        activity = "Python"
        email = "user@example.com"

        # Act
        response = app.signup_for_activity(activity, email)

        # Assert
        assert response["message"] == "Inscrição realizada com sucesso."
        assert email in app.activities[activity]["participants"]

    def test_signup_duplicate(self):
        # Arrange
        activity = "Python"
        email = "user@example.com"
        app.signup_for_activity(activity, email)

        # Act & Assert
        with pytest.raises(ValueError) as exc:
            app.signup_for_activity(activity, email)
        assert "já está inscrito" in str(exc.value)

    def test_signup_activity_not_found(self):
        # Arrange
        activity = "Inexistente"
        email = "user@example.com"

        # Act & Assert
        with pytest.raises(ValueError) as exc:
            app.signup_for_activity(activity, email)
        assert "não encontrada" in str(exc.value)

# Testes para remove_participant
class TestRemoveParticipant:
    def test_remove_success(self):
        # Arrange
        activity = "GitHub"
        email = "user@example.com"
        app.signup_for_activity(activity, email)

        # Act
        response = app.remove_participant(activity, email)

        # Assert
        assert response["message"] == "Participante removido com sucesso."
        assert email not in app.activities[activity]["participants"]

    def test_remove_not_signed_up(self):
        # Arrange
        activity = "GitHub"
        email = "user@example.com"

        # Act & Assert
        with pytest.raises(ValueError) as exc:
            app.remove_participant(activity, email)
        assert "não está inscrito" in str(exc.value)

    def test_remove_activity_not_found(self):
        # Arrange
        activity = "Inexistente"
        email = "user@example.com"

        # Act & Assert
        with pytest.raises(ValueError) as exc:
            app.remove_participant(activity, email)
        assert "não encontrada" in str(exc.value)

# Teste para get_activities
class TestGetActivities:
    def test_get_activities(self):
        # Arrange
        # Nenhuma preparação extra necessária, pois o fixture já inicializa as atividades

        # Act
        result = app.get_activities()

        # Assert
        assert isinstance(result, dict)
        assert "Python" in result
        assert "GitHub" in result
