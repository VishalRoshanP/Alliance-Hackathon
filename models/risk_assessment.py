"""Risk assessment model."""
from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from models.database import Base


class RiskAssessment(Base):
    """Risk assessment model."""
    __tablename__ = "risk_assessments"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    risk_score = Column(Float, nullable=False)  # 0-100
    risk_level = Column(String(20), nullable=False)  # low, medium, high, critical
    factors = Column(JSON)  # JSON object with risk factors and scores
    calculated_at = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    student = relationship("Student", back_populates="risk_assessments")
    interventions = relationship("Intervention", back_populates="risk_assessment")
