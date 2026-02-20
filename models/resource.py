"""Resource models."""
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from models.database import Base


class Resource(Base):
    """Resource model."""
    __tablename__ = "resources"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    type = Column(String(50), nullable=False)
    category = Column(String(100))
    description = Column(Text)
    eligibility_criteria = Column(Text)
    application_process = Column(Text)
    contact_info = Column(JSON)  # {email, phone, website, address}
    location = Column(String(200))
    availability = Column(String(20), default="available")
    tags = Column(JSON)  # Array of tags
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    recommendations = relationship("ResourceRecommendation", back_populates="resource")


class ResourceRecommendation(Base):
    """Resource recommendation model."""
    __tablename__ = "resource_recommendations"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=True)
    resource_id = Column(Integer, ForeignKey("resources.id"), nullable=False)
    recommended_at = Column(DateTime(timezone=True), server_default=func.now())
    student_viewed = Column(String(10), default="false")
    student_applied = Column(String(10), default="false")
    outcome = Column(String(50), nullable=True)
    
    # Relationships
    student = relationship("Student", back_populates="resource_recommendations")
    conversation = relationship("Conversation", back_populates="resource_recommendations")
    resource = relationship("Resource", back_populates="recommendations")
