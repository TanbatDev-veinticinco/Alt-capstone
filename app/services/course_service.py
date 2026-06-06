from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.models.course import Course
from app.repositories import course_repository
from app.schemas.course import CourseCreate, CourseUpdate


def get_active_courses(db: Session) -> List[Course]:
    return course_repository.get_active_courses(db)


def get_course(db: Session, course_id: int) -> Course:
    course = course_repository.get_course_by_id(db, course_id)

    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )

    return course


def create_course(db: Session, course_data: CourseCreate) -> Course:
    existing_course = course_repository.get_course_by_code(db, course_data.code)

    if existing_course:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Course code already exists"
        )

    return course_repository.create_course(db, course_data)


def update_course(db: Session, course_id: int, course_data: CourseUpdate) -> Course:
    course = course_repository.get_course_by_id(db, course_id)

    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )

    if course_data.code and course_data.code != course.code:
        existing_course = course_repository.get_course_by_code(db, course_data.code)

        if existing_course:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Course code already exists"
            )

    return course_repository.update_course(db, course, course_data)


def delete_course(db: Session, course_id: int) -> dict:
    course = course_repository.get_course_by_id(db, course_id)

    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )

    course_repository.delete_course(db, course)

    return {"message": "Course deleted successfully"}