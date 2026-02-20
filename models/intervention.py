"""Intervention model."""
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from models.database import Base


class Intervention(Base):
    """Intervention model."""
    __tablename__ = "interventions"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    risk_assessment_id = Column(Integer, ForeignKey("risk_assessments.id"), nullable=True)
    type = Column(String(50), nullable=False)
    status = Column(String(20), default="pending")
    recommended_resources = Column(JSON)  # Array of resource IDs
    action_plan = Column(Text)
    assigned_to = Column(Integer, nullable=True)  # Counselor/admin ID
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    outcome = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    student = relationship("Student", back_populates="interventions")
    risk_assessment = relationship("RiskAssessment", back_populates="interventions")
