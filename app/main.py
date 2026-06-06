from fastapi import FastAPI

from app.api.v1 import auth, courses, enrollments


app = FastAPI(
    title="Course Enrollment Platform API",
    description="FastAPI backend for course enrollment with authentication and RBAC.",
    version="1.0.0",
)


app.include_router(auth.router, prefix="/api/v1")
app.include_router(courses.router, prefix="/api/v1")
app.include_router(enrollments.router, prefix="/api/v1")


@app.get("/")
def read_root():
    return {"message": "Course Enrollment Platform API is running"}