from tests.conftest import create_test_course


def test_list_active_courses_public(client, db_session):
    create_test_course(db_session, code="PY101")
    create_test_course(db_session, title="Inactive Course", code="IN101", is_active=False)

    response = client.get("/api/v1/courses/")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["code"] == "PY101"


def test_get_course_by_id_public(client, db_session):
    course = create_test_course(db_session)

    response = client.get(f"/api/v1/courses/{course.id}")

    assert response.status_code == 200
    assert response.json()["id"] == course.id


def test_get_missing_course_returns_404(client):
    response = client.get("/api/v1/courses/999")

    assert response.status_code == 404


def test_admin_can_create_course(admin_client):
    response = admin_client.post(
        "/api/v1/courses/",
        json={"title": "Data Science", "code": "DS101", "capacity": 40},
    )

    assert response.status_code == 201
    assert response.json()["code"] == "DS101"


def test_student_cannot_create_course(student_client):
    response = student_client.post(
        "/api/v1/courses/",
        json={"title": "Data Science", "code": "DS101", "capacity": 40},
    )

    assert response.status_code == 403


def test_create_course_requires_auth(client):
    response = client.post(
        "/api/v1/courses/",
        json={"title": "Data Science", "code": "DS101", "capacity": 40},
    )

    assert response.status_code == 401


def test_duplicate_course_code_fails(admin_client, db_session):
    create_test_course(db_session, code="DS101")

    response = admin_client.post(
        "/api/v1/courses/",
        json={"title": "Data Science", "code": "DS101", "capacity": 40},
    )

    assert response.status_code == 400


def test_course_capacity_must_be_positive(admin_client):
    response = admin_client.post(
        "/api/v1/courses/",
        json={"title": "Bad Capacity", "code": "BAD101", "capacity": 0},
    )

    assert response.status_code == 422


def test_admin_can_update_course(admin_client, db_session):
    course = create_test_course(db_session)

    response = admin_client.put(
        f"/api/v1/courses/{course.id}",
        json={"title": "Advanced Python", "capacity": 50, "is_active": False},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Advanced Python"
    assert data["capacity"] == 50
    assert data["is_active"] is False


def test_student_cannot_update_course(student_client, db_session):
    course = create_test_course(db_session)

    response = student_client.put(
        f"/api/v1/courses/{course.id}",
        json={"title": "Not Allowed"},
    )

    assert response.status_code == 403


def test_admin_can_delete_course(admin_client, db_session):
    course = create_test_course(db_session)

    response = admin_client.delete(f"/api/v1/courses/{course.id}")

    assert response.status_code == 200
    assert response.json()["message"] == "Course deleted successfully"


def test_delete_missing_course_returns_404(admin_client):
    response = admin_client.delete("/api/v1/courses/999")

    assert response.status_code == 404
