from app.models.user import UserRole
from tests.conftest import create_test_user, login


def test_register_student_success(client):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "name": "Jane Student",
            "email": "jane@example.com",
            "password": "password123",
            "role": "student",
        },
    )

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Jane Student"
    assert data["email"] == "jane@example.com"
    assert data["role"] == "student"
    assert "password" not in data
    assert "hashed_password" not in data


def test_register_duplicate_email_fails(client):
    payload = {
        "name": "Jane Student",
        "email": "jane@example.com",
        "password": "password123",
        "role": "student",
    }

    first_response = client.post("/api/v1/auth/register", json=payload)
    second_response = client.post("/api/v1/auth/register", json=payload)

    assert first_response.status_code == 201
    assert second_response.status_code == 400


def test_register_invalid_role_fails(client):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "name": "Wrong Role",
            "email": "wrong@example.com",
            "password": "password123",
            "role": "teacher",
        },
    )

    assert response.status_code == 422


def test_register_short_password_fails(client):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "name": "Short Password",
            "email": "short@example.com",
            "password": "short",
            "role": "student",
        },
    )

    assert response.status_code == 422


def test_login_sets_http_only_cookie(client, student_user):
    response = login(client, student_user.email)

    assert response.status_code == 200
    assert response.json()["message"] == "Login successful"
    assert "access_token" in response.cookies
    assert "httponly" in response.headers["set-cookie"].lower()


def test_login_wrong_password_fails(client, student_user):
    response = login(client, student_user.email, password="wrongpass")

    assert response.status_code == 401


def test_inactive_user_cannot_login(client, db_session):
    user = create_test_user(
        db_session,
        email="inactive@example.com",
        role=UserRole.student,
        is_active=False,
    )

    response = login(client, user.email)

    assert response.status_code == 400


def test_get_profile_with_cookie_success(student_client, student_user):
    response = student_client.get("/api/v1/auth/me")

    assert response.status_code == 200
    assert response.json()["email"] == student_user.email


def test_get_profile_without_cookie_fails(client):
    response = client.get("/api/v1/auth/me")

    assert response.status_code == 401


def test_logout_deletes_cookie(student_client):
    response = student_client.post("/api/v1/auth/logout")

    assert response.status_code == 200
    assert response.json()["message"] == "Logged out successfully"
