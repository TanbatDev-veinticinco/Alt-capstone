from app.models.user import UserRole
from tests.conftest import create_test_course, create_test_user, login


def test_student_can_enroll(student_client, db_session):
    course = create_test_course(db_session)

    response = student_client.post(f"/api/v1/enrollments/{course.id}")

    assert response.status_code == 201
    data = response.json()
    assert data["course_id"] == course.id
    assert data["user"]["role"] == "student"
    assert data["course"]["code"] == course.code


def test_admin_cannot_enroll(admin_client, db_session):
    course = create_test_course(db_session)

    response = admin_client.post(f"/api/v1/enrollments/{course.id}")

    assert response.status_code == 403


def test_unauthenticated_user_cannot_enroll(client, db_session):
    course = create_test_course(db_session)

    response = client.post(f"/api/v1/enrollments/{course.id}")

    assert response.status_code == 401


def test_student_cannot_enroll_twice(student_client, db_session):
    course = create_test_course(db_session)

    first_response = student_client.post(f"/api/v1/enrollments/{course.id}")
    second_response = student_client.post(f"/api/v1/enrollments/{course.id}")

    assert first_response.status_code == 201
    assert second_response.status_code == 400


def test_student_cannot_enroll_in_inactive_course(student_client, db_session):
    course = create_test_course(db_session, is_active=False)

    response = student_client.post(f"/api/v1/enrollments/{course.id}")

    assert response.status_code == 400


def test_student_cannot_enroll_in_full_course(client, db_session):
    course = create_test_course(db_session, capacity=1)
    first_student = create_test_user(db_session, email="one@example.com")
    second_student = create_test_user(db_session, email="two@example.com")

    login(client, first_student.email)
    first_response = client.post(f"/api/v1/enrollments/{course.id}")
    client.post("/api/v1/auth/logout")

    login(client, second_student.email)
    second_response = client.post(f"/api/v1/enrollments/{course.id}")

    assert first_response.status_code == 201
    assert second_response.status_code == 400


def test_student_can_deregister(student_client, db_session):
    course = create_test_course(db_session)
    student_client.post(f"/api/v1/enrollments/{course.id}")

    response = student_client.delete(f"/api/v1/enrollments/{course.id}")

    assert response.status_code == 200
    assert response.json()["message"] == "Successfully deregistered from course"


def test_student_cannot_deregister_if_not_enrolled(student_client, db_session):
    course = create_test_course(db_session)

    response = student_client.delete(f"/api/v1/enrollments/{course.id}")

    assert response.status_code == 404


def test_admin_can_view_all_enrollments(client, db_session, admin_user):
    course = create_test_course(db_session)
    student = create_test_user(db_session, email="enrolled@example.com")

    login(client, student.email)
    client.post(f"/api/v1/enrollments/{course.id}")
    client.post("/api/v1/auth/logout")

    login(client, admin_user.email)
    response = client.get("/api/v1/enrollments/")

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_student_cannot_view_all_enrollments(student_client):
    response = student_client.get("/api/v1/enrollments/")

    assert response.status_code == 403


def test_admin_can_view_course_enrollments(client, db_session, admin_user):
    course = create_test_course(db_session)
    student = create_test_user(db_session, email="course-view@example.com")

    login(client, student.email)
    client.post(f"/api/v1/enrollments/{course.id}")
    client.post("/api/v1/auth/logout")

    login(client, admin_user.email)
    response = client.get(f"/api/v1/enrollments/course/{course.id}")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["course_id"] == course.id


def test_admin_can_remove_student_from_course(client, db_session, admin_user):
    course = create_test_course(db_session)
    student = create_test_user(db_session, email="remove@example.com", role=UserRole.student)

    login(client, student.email)
    client.post(f"/api/v1/enrollments/{course.id}")
    client.post("/api/v1/auth/logout")

    login(client, admin_user.email)
    response = client.delete(f"/api/v1/enrollments/{course.id}/students/{student.id}")

    assert response.status_code == 200
    assert response.json()["message"] == "Student removed from course successfully"


def test_student_cannot_remove_student_from_course(student_client, db_session):
    course = create_test_course(db_session)
    other_student = create_test_user(db_session, email="other@example.com")

    response = student_client.delete(
        f"/api/v1/enrollments/{course.id}/students/{other_student.id}"
    )

    assert response.status_code == 403
