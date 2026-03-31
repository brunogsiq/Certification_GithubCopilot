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
        response = app.signup_for_activity("Python", "user@example.com")
        assert response["message"] == "Inscrição realizada com sucesso."
        assert "user@example.com" in app.activities["Python"]["participants"]

    def test_signup_duplicate(self):
        app.signup_for_activity("Python", "user@example.com")
        with pytest.raises(ValueError) as exc:
            app.signup_for_activity("Python", "user@example.com")
        assert "já está inscrito" in str(exc.value)

    def test_signup_activity_not_found(self):
        with pytest.raises(ValueError) as exc:
            app.signup_for_activity("Inexistente", "user@example.com")
        assert "não encontrada" in str(exc.value)

# Testes para remove_participant
class TestRemoveParticipant:
    def test_remove_success(self):
        app.signup_for_activity("GitHub", "user@example.com")
        response = app.remove_participant("GitHub", "user@example.com")
        assert response["message"] == "Participante removido com sucesso."
        assert "user@example.com" not in app.activities["GitHub"]["participants"]

    def test_remove_not_signed_up(self):
        with pytest.raises(ValueError) as exc:
            app.remove_participant("GitHub", "user@example.com")
        assert "não está inscrito" in str(exc.value)

    def test_remove_activity_not_found(self):
        with pytest.raises(ValueError) as exc:
            app.remove_participant("Inexistente", "user@example.com")
        assert "não encontrada" in str(exc.value)

# Teste para get_activities
class TestGetActivities:
    def test_get_activities(self):
        result = app.get_activities()
        assert isinstance(result, dict)
        assert "Python" in result
        assert "GitHub" in result
