"""Student model."""
from sqlalchemy import Column, Integer, String, Date, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from models.database import Base


class Student(Base):
    """Student model."""
    __tablename__ = "students"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(200), nullable=False)
    age = Column(Integer)
    gender = Column(String(10))
    email = Column(String(255))
    phone = Column(String(20))
    address = Column(Text)
    school_id = Column(Integer, ForeignKey("schools.id"))
    grade_level = Column(String(50))
    enrollment_date = Column(Date)
    status = Column(String(20), default="active")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    school = relationship("School", back_populates="students")
    conversations = relationship("Conversation", back_populates="student")
    risk_assessments = relationship("RiskAssessment", back_populates="student")
    interventions = relationship("Intervention", back_populates="student")
    attendance_records = relationship("AttendanceRecord", back_populates="student")
    fee_records = relationship("FeeRecord", back_populates="student")
    health_records = relationship("HealthRecord", back_populates="student")
    academic_records = relationship("AcademicRecord", back_populates="student")
    resource_recommendations = relationship("ResourceRecommendation", back_populates="student")
