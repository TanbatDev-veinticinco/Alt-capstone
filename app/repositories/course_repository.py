from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.course import Course
from app.schemas.course import CourseCreate, CourseUpdate

def get_active_courses(db: Session) -> List[Course]:
    return db.query(Course).filter(Course.is_active.is_(True)).all()


def get_all_courses(db: Session) -> List[Course]:
    return db.query(Course).all()

def get_course_by_id(db:Session, course_id: int) -> Optional[Course]:
    return db.query(Course).filter(Course.id == course_id).first()

def get_course_by_code(db:Session, code: str) -> Optional[Course]:
    return db.query(Course).filter(Course.code == code).first()

def create_course(db: Session, course_data: CourseCreate) -> Course:
    db_course = Course(
        title=course_data.title,
        code=course_data.code,
        capacity=course_data.capacity,
        is_active=True
    )

    db.add(db_course)
    db.commit()
    db.refresh(db_course)

    return db_course

def update_course(db: Session, course: Course, course_data: CourseUpdate) -> Course:
    if course_data.title is not None:
        course.title = course_data.title
    if course_data.code is not None:
        course.code = course_data.code
    if course_data.capacity is not None:
        course.capacity = course_data.capacity
    if course_data.is_active is not None:
        course.is_active = course_data.is_active

    db.commit()
    db.refresh(course)

    return course

def delete_course(db: Session, course: Course) -> None:
    """Permanently delete a course from the database"""
    db.delete(course)
    db.commit()