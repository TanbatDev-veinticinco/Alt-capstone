import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app
from app.models.course import Course
from app.models.enrollment import Enrollment
from app.models.user import User, UserRole
from app.repositories.user_repository import hash_password


SQLALCHEMY_TEST_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


def create_test_user(
    db_session,
    email="student@example.com",
    name="Test Student",
    role=UserRole.student,
    password="password123",
    is_active=True,
):
    user = User(
        name=name,
        email=email,
        hashed_password=hash_password(password),
        role=role,
        is_active=is_active,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


def create_test_course(
    db_session,
    title="Python Basics",
    code="PY101",
    capacity=30,
    is_active=True,
):
    course = Course(
        title=title,
        code=code,
        capacity=capacity,
        is_active=is_active,
    )
    db_session.add(course)
    db_session.commit()
    db_session.refresh(course)
    return course


def login(client, email, password="password123"):
    return client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": password},
    )


@pytest.fixture
def student_user(db_session):
    return create_test_user(db_session)


@pytest.fixture
def admin_user(db_session):
    return create_test_user(
        db_session,
        email="admin@example.com",
        name="Test Admin",
        role=UserRole.admin,
    )


@pytest.fixture
def student_client(client, student_user):
    login(client, student_user.email)
    return client


@pytest.fixture
def admin_client(client, admin_user):
    login(client, admin_user.email)
    return client
