"""School management API endpoints."""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.orm import Session

from models.database import get_db
from models.school import School
from utils.logger import setup_logger

logger = setup_logger()

router = APIRouter()


class SchoolCreate(BaseModel):
    """School creation model."""
    name: str
    code: str
    type: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = "India"
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None


class SchoolUpdate(BaseModel):
    """School update model."""
    name: Optional[str] = None
    type: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None


@router.get("")
async def list_schools(
    limit: int = 100,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """List all schools."""
    try:
        schools = db.query(School).offset(offset).limit(limit).all()
        total = db.query(School).count()
        
        return {
            "schools": [
                {
                    "id": s.id,
                    "name": s.name,
                    "code": s.code,
                    "type": s.type,
                    "city": s.city,
                    "state": s.state,
                    "country": s.country,
                    "contact_email": s.contact_email,
                    "contact_phone": s.contact_phone
                }
                for s in schools
            ],
            "total": total,
            "limit": limit,
            "offset": offset
        }
    except Exception as e:
        logger.error(f"Error listing schools: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{school_id}")
async def get_school(
    school_id: int,
    db: Session = Depends(get_db)
):
    """Get school details."""
    try:
        school = db.query(School).filter(School.id == school_id).first()
        
        if not school:
            raise HTTPException(status_code=404, detail="School not found")
        
        return {
            "id": school.id,
            "name": school.name,
            "code": school.code,
            "type": school.type,
            "address": school.address,
            "city": school.city,
            "state": school.state,
            "country": school.country,
            "contact_email": school.contact_email,
            "contact_phone": school.contact_phone,
            "created_at": school.created_at.isoformat() if school.created_at else None
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting school: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("")
async def create_school(
    school_data: SchoolCreate,
    db: Session = Depends(get_db)
):
    """Register a new school."""
    try:
        # Check if code already exists
        existing = db.query(School).filter(School.code == school_data.code).first()
        
        if existing:
            raise HTTPException(status_code=400, detail="School code already exists")
        
        school = School(**school_data.dict())
        db.add(school)
        db.commit()
        db.refresh(school)
        
        return {
            "id": school.id,
            "name": school.name,
            "code": school.code,
            "status": "created"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating school: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{school_id}")
async def update_school(
    school_id: int,
    school_data: SchoolUpdate,
    db: Session = Depends(get_db)
):
    """Update school information."""
    try:
        school = db.query(School).filter(School.id == school_id).first()
        
        if not school:
            raise HTTPException(status_code=404, detail="School not found")
        
        # Update fields
        update_data = school_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(school, field, value)
        
        db.commit()
        db.refresh(school)
        
        return {
            "id": school.id,
            "name": school.name,
            "status": "updated"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating school: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{school_id}/students")
async def get_school_students(
    school_id: int,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all students for a school."""
    try:
        from models.student import Student
        
        students = db.query(Student).filter(
            Student.school_id == school_id
        ).limit(limit).all()
        
        return {
            "school_id": school_id,
            "students": [
                {
                    "id": s.id,
                    "student_id": s.student_id,
                    "name": s.name,
                    "status": s.status
                }
                for s in students
            ],
            "count": len(students)
        }
    except Exception as e:
        logger.error(f"Error getting school students: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{school_id}/stats")
async def get_school_stats(
    school_id: int,
    db: Session = Depends(get_db)
):
    """Get school statistics."""
    try:
        from models.student import Student
        from models.risk_assessment import RiskAssessment
        
        total_students = db.query(Student).filter(
            Student.school_id == school_id
        ).count()
        
        at_risk_students = db.query(Student).filter(
            Student.school_id == school_id,
            Student.status == "at_risk"
        ).count()
        
        # Get risk distribution
        risk_query = db.query(RiskAssessment).join(Student).filter(
            Student.school_id == school_id
        )
        
        risk_distribution = {
            "low": risk_query.filter(RiskAssessment.risk_level == "low").count(),
            "medium": risk_query.filter(RiskAssessment.risk_level == "medium").count(),
            "high": risk_query.filter(RiskAssessment.risk_level == "high").count(),
            "critical": risk_query.filter(RiskAssessment.risk_level == "critical").count()
        }
        
        return {
            "school_id": school_id,
            "total_students": total_students,
            "at_risk_students": at_risk_students,
            "risk_distribution": risk_distribution,
            "at_risk_percentage": round((at_risk_students / total_students * 100) if total_students > 0 else 0, 2)
        }
    except Exception as e:
        logger.error(f"Error getting school stats: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
