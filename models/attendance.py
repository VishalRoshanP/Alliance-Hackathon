"""Attendance record model."""
from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from models.database import Base


class AttendanceRecord(Base):
    """Attendance record model."""
    __tablename__ = "attendance_records"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    date = Column(Date, nullable=False)
    status = Column(String(20), nullable=False)  # present, absent, late, excused
    reason = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Unique constraint on student_id and date
    __table_args__ = (UniqueConstraint('student_id', 'date', name='unique_student_date'),)
    
    # Relationships
    student = relationship("Student", back_populates="attendance_records")
