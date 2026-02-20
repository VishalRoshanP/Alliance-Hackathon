"""Student management API endpoints."""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy.orm import Session
from datetime import date

from models.database import get_db
from models.student import Student
from core.risk_analyzer import risk_analyzer
from utils.logger import setup_logger

logger = setup_logger()

router = APIRouter()


class StudentCreate(BaseModel):
    """Student creation model."""
    student_id: str
    name: str
    age: Optional[int] = None
    gender: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    school_id: Optional[int] = None
    grade_level: Optional[str] = None
    enrollment_date: Optional[date] = None


class StudentUpdate(BaseModel):
    """Student update model."""
    name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    school_id: Optional[int] = None
    grade_level: Optional[str] = None
    status: Optional[str] = None


@router.get("")
async def list_students(
    school_id: Optional[int] = None,
    status: Optional[str] = None,
    limit: int = 100,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """List students with filters."""
    try:
        query = db.query(Student)
        
        if school_id:
            query = query.filter(Student.school_id == school_id)
        
        if status:
            query = query.filter(Student.status == status)
        
        total = query.count()
        students = query.offset(offset).limit(limit).all()
        
        return {
            "students": [
                {
                    "id": s.id,
                    "student_id": s.student_id,
                    "name": s.name,
                    "age": s.age,
                    "gender": s.gender,
                    "email": s.email,
                    "phone": s.phone,
                    "school_id": s.school_id,
                    "grade_level": s.grade_level,
                    "status": s.status,
                    "enrollment_date": s.enrollment_date.isoformat() if s.enrollment_date else None
                }
                for s in students
            ],
            "total": total,
            "limit": limit,
            "offset": offset
        }
    except Exception as e:
        logger.error(f"Error listing students: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{student_id}")
async def get_student(
    student_id: int,
    db: Session = Depends(get_db)
):
    """Get student details."""
    try:
        student = db.query(Student).filter(Student.id == student_id).first()
        
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        
        return {
            "id": student.id,
            "student_id": student.student_id,
            "name": student.name,
            "age": student.age,
            "gender": student.gender,
            "email": student.email,
            "phone": student.phone,
            "address": student.address,
            "school_id": student.school_id,
            "grade_level": student.grade_level,
            "status": student.status,
            "enrollment_date": student.enrollment_date.isoformat() if student.enrollment_date else None,
            "created_at": student.created_at.isoformat() if student.created_at else None
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting student: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("")
async def create_student(
    student_data: StudentCreate,
    db: Session = Depends(get_db)
):
    """Create a new student."""
    try:
        # Check if student_id already exists
        existing = db.query(Student).filter(
            Student.student_id == student_data.student_id
        ).first()
        
        if existing:
            raise HTTPException(status_code=400, detail="Student ID already exists")
        
        student = Student(**student_data.dict())
        db.add(student)
        db.commit()
        db.refresh(student)
        
        return {
            "id": student.id,
            "student_id": student.student_id,
            "name": student.name,
            "status": "created"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating student: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{student_id}")
async def update_student(
    student_id: int,
    student_data: StudentUpdate,
    db: Session = Depends(get_db)
):
    """Update student information."""
    try:
        student = db.query(Student).filter(Student.id == student_id).first()
        
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        
        # Update fields
        update_data = student_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(student, field, value)
        
        db.commit()
        db.refresh(student)
        
        return {
            "id": student.id,
            "student_id": student.student_id,
            "name": student.name,
            "status": "updated"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating student: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{student_id}")
async def delete_student(
    student_id: int,
    db: Session = Depends(get_db)
):
    """Delete a student."""
    try:
        student = db.query(Student).filter(Student.id == student_id).first()
        
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        
        db.delete(student)
        db.commit()
        
        return {"status": "deleted", "student_id": student_id}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting student: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{student_id}/risk")
async def get_student_risk(
    student_id: int,
    db: Session = Depends(get_db)
):
    """Get student's risk assessment."""
    try:
        student = db.query(Student).filter(Student.id == student_id).first()
        
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        
        risk_assessment = risk_analyzer.calculate_risk_score(db, student_id)
        
        return {
            "student_id": student_id,
            "risk_assessment": risk_assessment
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting student risk: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{student_id}/history")
async def get_student_history(
    student_id: int,
    db: Session = Depends(get_db)
):
    """Get student's complete history."""
    try:
        student = db.query(Student).filter(Student.id == student_id).first()
        
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        
        return {
            "student": {
                "id": student.id,
                "student_id": student.student_id,
                "name": student.name,
                "status": student.status
            },
            "conversations": len(student.conversations),
            "risk_assessments": len(student.risk_assessments),
            "interventions": len(student.interventions),
            "attendance_records": len(student.attendance_records),
            "fee_records": len(student.fee_records),
            "health_records": len(student.health_records),
            "academic_records": len(student.academic_records)
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting student history: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
