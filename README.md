# Course Enrollment Platform API

A secure, database-backed REST API built with FastAPI for managing courses and student enrollments.

The API supports user registration, login with JWT stored in an HTTP-only cookie, role-based access control, course management, enrollment rules, database migrations, and automated tests.

## Features

- User registration and login
- JWT authentication using HTTP-only cookies
- Role-based access control for students and admins
- Public course listing and course detail endpoints
- Admin-only course create, update, deactivate, and delete actions
- Student-only course enrollment and deregistration
- Admin oversight for all enrollments
- PostgreSQL database support
- Alembic migrations
- Automated API tests with pytest

## Project Structure

```text
app/
  api/v1/              API route handlers
  models/              SQLAlchemy database models
  schemas/             Pydantic request and response schemas
  repositories/        Database access layer
  services/            Business logic layer
  config.py            App settings loaded from .env
  database.py          Database engine, session, and Base setup
  main.py              FastAPI app entry point
migrations/            Alembic migration files
tests/                 Automated API tests
```

## Setup

Create and activate a virtual environment:

```bash
python -m venv env
```

On Windows PowerShell:

```powershell
.\env\Scripts\Activate.ps1
```

On Git Bash:

```bash
source env/Scripts/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql://postgres:YourPassword@localhost:5432/enrollment_db
SECRET_KEY=make-this-a-very-long-random-string-like-this-one-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Update `DATABASE_URL` with your real PostgreSQL username, password, host, port, and database name.

## Database Migrations

Generate a migration after model changes:

```bash
alembic revision --autogenerate -m "initial tables"
```

Run migrations:

```bash
alembic upgrade head
```

Check migration history:

```bash
alembic history
```

## Run The App

Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

Open the API documentation:

```text
http://127.0.0.1:8000/docs
```

## Run Tests

Run all tests:

```bash
python -m pytest tests -v
```

If pytest cache permissions cause warnings, run:

```bash
python -m pytest tests -v -p no:cacheprovider
```

## API Endpoints

### Authentication

| Method | Endpoint | Access | Description |
| --- | --- | --- | --- |
| POST | `/api/v1/auth/register` | Public | Register a new user |
| POST | `/api/v1/auth/login` | Public | Log in and set JWT cookie |
| GET | `/api/v1/auth/me` | Authenticated | Get current user profile |
| POST | `/api/v1/auth/logout` | Authenticated | Clear login cookie |

### Courses

| Method | Endpoint | Access | Description |
| --- | --- | --- | --- |
| GET | `/api/v1/courses/` | Public | List active courses |
| GET | `/api/v1/courses/{course_id}` | Public | Get course by ID |
| POST | `/api/v1/courses/` | Admin | Create course |
| PUT | `/api/v1/courses/{course_id}` | Admin | Update course |
| DELETE | `/api/v1/courses/{course_id}` | Admin | Delete course |

### Enrollments

| Method | Endpoint | Access | Description |
| --- | --- | --- | --- |
| POST | `/api/v1/enrollments/{course_id}` | Student | Enroll in a course |
| DELETE | `/api/v1/enrollments/{course_id}` | Student | Deregister from a course |
| GET | `/api/v1/enrollments/` | Admin | View all enrollments |
| GET | `/api/v1/enrollments/course/{course_id}` | Admin | View enrollments for a course |
| DELETE | `/api/v1/enrollments/{course_id}/students/{user_id}` | Admin | Remove student from course |

## Business Rules

- Email addresses must be unique.
- Passwords are securely hashed before storage.
- User role must be either `student` or `admin`.
- Inactive users cannot authenticate.
- Course codes must be unique.
- Course capacity must be greater than zero.
- Only admins can create, update, and delete courses.
- Only students can enroll in and deregister from courses.
- Students cannot enroll in the same course twice.
- Students cannot enroll in inactive courses.
- Students cannot enroll in full courses.
- Admins can view and manage enrollments.
