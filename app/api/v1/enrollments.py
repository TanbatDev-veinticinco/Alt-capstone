from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.user import User
from app.schemas.enrollment import EnrollmentResponse
from app.services import enrollment_service
from app.services.auth_service import require_admin, require_student


router = APIRouter(prefix="/enrollments", tags=["Enrollments"])


@router.post("/{course_id}", response_model=EnrollmentResponse, status_code=status.HTTP_201_CREATED)
def enroll(
    course_id: int,
    db: Session = Depends(get_db),
    current_student: User = Depends(require_student)
):
    return enrollment_service.enroll_student(db, current_student, course_id)


@router.delete("/{course_id}", status_code=status.HTTP_200_OK)
def deregister(
    course_id: int,
    db: Session = Depends(get_db),
    current_student: User = Depends(require_student)
):
    return enrollment_service.deregister_student(db, current_student, course_id)


@router.get("/", response_model=List[EnrollmentResponse])
def get_all_enrollments(
    db: Session = Depends(get_db),
    current_admin: User = Depends(require_admin)
):
    return enrollment_service.get_all_enrollments(db)


@router.get("/course/{course_id}", response_model=List[EnrollmentResponse])
def get_course_enrollments(
    course_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(require_admin)
):
    return enrollment_service.get_course_enrollments(db, course_id)


@router.delete("/{course_id}/students/{user_id}", status_code=status.HTTP_200_OK)
def admin_remove_student(
    course_id: int,
    user_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(require_admin)
):
    return enrollment_service.admin_remove_student(db, course_id, user_id)