"""Health record model."""
from sqlalchemy import Column, Integer, String, Date, Boolean, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from models.database import Base


class HealthRecord(Base):
    """Health record model."""
    __tablename__ = "health_records"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    issue_type = Column(String(100))  # chronic, acute, mental_health
    description = Column(Text)
    severity = Column(String(20))  # low, medium, high, critical
    affects_attendance = Column(Boolean, default=False)
    reported_date = Column(Date)
    resolved_date = Column(Date, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    student = relationship("Student", back_populates="health_records")
