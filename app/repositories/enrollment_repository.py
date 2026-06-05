from sqlalchemy.orm import Session, joinedload
from typing import List, Optional

from app.models.enrollment import Enrollment


def get_enrollment(db: Session, user_id: int, course_id: int) -> Optional[Enrollment]:
    return db.query(Enrollment).filter(
        Enrollment.user_id == user_id,
        Enrollment.course_id == course_id
    ).first()


def count_enrollments_for_course(db: Session, course_id: int) -> int:
    return db.query(Enrollment).filter(Enrollment.course_id == course_id).count()


def create_enrollment(db: Session, user_id: int, course_id: int) -> Enrollment:
    enrollment = Enrollment(user_id=user_id, course_id=course_id)

    db.add(enrollment)
    db.commit()
    db.refresh(enrollment)

    return db.query(Enrollment).options(
        joinedload(Enrollment.user),
        joinedload(Enrollment.course)
    ).filter(Enrollment.id == enrollment.id).first()


def delete_enrollment(db: Session, enrollment: Enrollment) -> None:
    db.delete(enrollment)
    db.commit()


def get_all_enrollments(db: Session) -> List[Enrollment]:
    return db.query(Enrollment).options(
        joinedload(Enrollment.user),
        joinedload(Enrollment.course)
    ).all()


def get_enrollments_by_course(db: Session, course_id: int) -> List[Enrollment]:
    return db.query(Enrollment).options(
        joinedload(Enrollment.user),
        joinedload(Enrollment.course)
    ).filter(Enrollment.course_id == course_id).all()