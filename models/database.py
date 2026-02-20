"""Database connection and setup."""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings
from utils.logger import setup_logger

logger = setup_logger()

# Create database engine
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


def get_db():
    """Get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database with all tables."""
    try:
        # Import all models to register them
        from models.student import Student
        from models.school import School
        from models.conversation import Conversation, Message
        from models.risk_assessment import RiskAssessment
        from models.intervention import Intervention
        from models.resource import Resource, ResourceRecommendation
        from models.attendance import AttendanceRecord
        from models.fee import FeeRecord
        from models.health import HealthRecord
        from models.academic import AcademicRecord
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error initializing database: {str(e)}")
        raise
