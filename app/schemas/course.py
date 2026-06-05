from pydantic import BaseModel, field_validator
from typing import Optional

class CourseCreate(BaseModel):
    title: str 
    code: str 
    capacity: int


    @field_validator("capacity")
    @classmethod
    def validate_capacity(cls, value):
        if value < 1:
            raise ValueError("capacity must be at least 1")
        return value
    
    @field_validator("title")
    @classmethod
    def validate_title(cls, value):
        if not value.strip():
            raise ValueError("title cannot be empty")
        return value.strip()


    @field_validator("code")
    @classmethod
    def validate_code(cls, value):
        if not value.strip():
            raise ValueError("code cannot be empty")
        return value.strip().upper()

    
class CourseUpdate(BaseModel):
    title: Optional[str] = None
    code: Optional[str] = None
    capacity: Optional[int] = None
    is_active: Optional[bool] = None

    @field_validator("capacity")
    @classmethod
    def validate_capacity(cls, value):
        if value is not None and value < 1:
            raise ValueError("capacity must be at least 1")
        return value
    

class CourseResponse(BaseModel):
    id: int
    title: str
    code: str
    capacity: int
    is_active: bool

    class Config:
        from_attributes = True

