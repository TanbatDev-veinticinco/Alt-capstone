from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.user import User
from app.schemas.course import CourseCreate, CourseUpdate, CourseResponse
from app.services import course_service
from app.services.auth_service import require_admin


router = APIRouter(prefix="/courses", tags=["Courses"])


@router.get("/", response_model=List[CourseResponse])
def list_active_courses(db: Session = Depends(get_db)):
    return course_service.get_active_courses(db)


@router.get("/{course_id}", response_model=CourseResponse)
def get_course(course_id: int, db: Session = Depends(get_db)):
    return course_service.get_course(db, course_id)


@router.post("/", response_model=CourseResponse, status_code=status.HTTP_201_CREATED)
def create_course(
    course_data: CourseCreate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(require_admin)
):
    return course_service.create_course(db, course_data)


@router.put("/{course_id}", response_model=CourseResponse)
def update_course(
    course_id: int,
    course_data: CourseUpdate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(require_admin)
):
    return course_service.update_course(db, course_id, course_data)


@router.delete("/{course_id}", status_code=status.HTTP_200_OK)
def delete_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(require_admin)
):
    return course_service.delete_course(db, course_id)