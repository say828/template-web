from fastapi.testclient import TestClient

from api.http.app import app


def test_health() -> None:
    with TestClient(app) as client:
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}


def test_status() -> None:
    with TestClient(app) as client:
        response = client.get("/api/v1/status")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"


def test_login_and_me() -> None:
    with TestClient(app) as client:
        login_response = client.post(
            "/api/v1/auth/login",
            json={"email": "admin@example.com", "password": "<CHANGE_ME>"},
        )
        assert login_response.status_code == 200
        token = login_response.json()["access_token"]

        me_response = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
        assert me_response.status_code == 200
        assert me_response.json()["email"] == "admin@example.com"


def test_users_context_examples() -> None:
    with TestClient(app) as client:
        login_response = client.post(
            "/api/v1/auth/login",
            json={"email": "admin@example.com", "password": "<CHANGE_ME>"},
        )
        assert login_response.status_code == 200
        headers = {"Authorization": f"Bearer {login_response.json()['access_token']}"}

        users_response = client.get("/api/v1/users", headers=headers)
        assert users_response.status_code == 200
        assert len(users_response.json()) == 2

        user_response = client.get("/api/v1/users/user-1", headers=headers)
        assert user_response.status_code == 200
        assert user_response.json()["timezone"] == "Asia/Seoul"
