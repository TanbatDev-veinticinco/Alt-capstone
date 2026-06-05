from datetime import datetime
from pydantic import BaseModel

from app.schemas.course import CourseResponse
from app.schemas.user import UserResponse


class EnrollmentResponse(BaseModel):
    id: int
    user_id: int
    course_id: int
    created_at: datetime
    user: UserResponse
    course: CourseResponse

    class Config: 
        from_attributes = True