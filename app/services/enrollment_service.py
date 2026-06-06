from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.models.enrollment import Enrollment
from app.models.user import User
from app.repositories import course_repository, enrollment_repository


def enroll_student(db: Session, student: User, course_id: int) -> Enrollment:
    course = course_repository.get_course_by_id(db, course_id)

    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )

    if not course.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot enroll in an inactive course"
        )

    existing_enrollment = enrollment_repository.get_enrollment(
        db,
        student.id,
        course_id
    )

    if existing_enrollment:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You are already enrolled in this course"
        )

    enrollment_count = enrollment_repository.count_enrollments_for_course(
        db,
        course_id
    )

    if enrollment_count >= course.capacity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Course is full"
        )

    return enrollment_repository.create_enrollment(db, student.id, course_id)


def deregister_student(db: Session, student: User, course_id: int) -> dict:
    course = course_repository.get_course_by_id(db, course_id)

    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )

    enrollment = enrollment_repository.get_enrollment(db, student.id, course_id)

    if not enrollment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="You are not enrolled in this course"
        )

    enrollment_repository.delete_enrollment(db, enrollment)

    return {"message": "Successfully deregistered from course"}


def get_all_enrollments(db: Session) -> List[Enrollment]:
    return enrollment_repository.get_all_enrollments(db)


def get_course_enrollments(db: Session, course_id: int) -> List[Enrollment]:
    course = course_repository.get_course_by_id(db, course_id)

    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )

    return enrollment_repository.get_enrollments_by_course(db, course_id)


def admin_remove_student(db: Session, course_id: int, user_id: int) -> dict:
    course = course_repository.get_course_by_id(db, course_id)

    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )

    enrollment = enrollment_repository.get_enrollment(db, user_id, course_id)

    if not enrollment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Enrollment not found"
        )

    enrollment_repository.delete_enrollment(db, enrollment)

    return {"message": "Student removed from course successfully"}