from sqlalchemy import Column, Integer, Boolean, String
from sqlalchemy.orm import relationship

from app.database import Base

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, nullable=False, index=True)
    title = Column(String, nullable=False, index=True)
    capacity = Column(Integer, nullable=False)
    is_active = Column(Boolean, default=True)

    enrollments = relationship("Enrollment", back_populates="course")