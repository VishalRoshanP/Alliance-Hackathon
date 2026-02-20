"""School model."""
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from models.database import Base


class School(Base):
    """School model."""
    __tablename__ = "schools"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    code = Column(String(50), unique=True, nullable=False, index=True)
    type = Column(String(50))  # primary, secondary, college
    address = Column(Text)
    city = Column(String(100))
    state = Column(String(100))
    country = Column(String(100), default="India")
    contact_email = Column(String(255))
    contact_phone = Column(String(20))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    students = relationship("Student", back_populates="school")
