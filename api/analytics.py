"""Analytics API endpoints."""
from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy.orm import Session
import pandas as pd

from models.database import get_db
from core.risk_analyzer import risk_analyzer
from services.file_upload_service import file_upload_service
from models.student import Student
from models.risk_assessment import RiskAssessment
from utils.logger import setup_logger

logger = setup_logger()

router = APIRouter()


class CalculateRiskRequest(BaseModel):
    """Request model for risk calculation."""
    student_id: int


@router.post("/upload-data")
async def upload_data(
    file: UploadFile = File(...),
    school_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Upload student data (CSV/Excel)."""
    try:
        # Save uploaded file
        file_path = await file_upload_service.save_upload_file(file)
        
        # Parse file based on extension
        if file.filename.endswith('.csv'):
            data = await file_upload_service.parse_csv(file_path)
        elif file.filename.endswith(('.xlsx', '.xls')):
            data = await file_upload_service.parse_excel(file_path)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file format")
        
        # Validate data
        valid_records, errors = file_upload_service.validate_student_data(data)
        
        # Process and save records
        processed_count = 0
        from models.student import Student
        from models.attendance import AttendanceRecord
        from models.fee import FeeRecord
        from models.health import HealthRecord
        
        for record in valid_records:
            try:
                # Find or create student
                student = db.query(Student).filter(
                    Student.student_id == str(record.get('student_id'))
                ).first()
                
                if not student:
                    student = Student(
                        student_id=str(record.get('student_id')),
                        name=record.get('name'),
                        school_id=school_id,
                        email=record.get('email'),
                        phone=record.get('phone'),
                        address=record.get('address'),
                        grade_level=record.get('grade_level')
                    )
                    db.add(student)
                    db.flush()
                
                # Process attendance if available
                if 'attendance' in record or 'attendance_%' in record:
                    # Add attendance logic here
                    pass
                
                # Process fees if available
                if 'fees_pending' in record or 'fee_pending' in record:
                    fee_amount = record.get('fees_pending') or record.get('fee_pending', 0)
                    if fee_amount and fee_amount > 0:
                        fee_record = FeeRecord(
                            student_id=student.id,
                            amount_due=float(fee_amount),
                            status="pending"
                        )
                        db.add(fee_record)
                
                # Process health issues if available
                if 'health_issues' in record and record.get('health_issues'):
                    health_record = HealthRecord(
                        student_id=student.id,
                        description=str(record.get('health_issues')),
                        severity="medium"
                    )
                    db.add(health_record)
                
                processed_count += 1
            except Exception as e:
                logger.error(f"Error processing record: {str(e)}")
                errors.append(f"Row {processed_count + 1}: {str(e)}")
        
        db.commit()
        
        return {
            "status": "success",
            "processed": processed_count,
            "errors": errors,
            "total_records": len(data)
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error uploading data: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/calculate-risk")
async def calculate_risk(
    request: CalculateRiskRequest,
    db: Session = Depends(get_db)
):
    """Calculate risk score for a student."""
    try:
        risk_assessment = risk_analyzer.calculate_risk_score(db, request.student_id)
        
        # Save risk assessment
        assessment = RiskAssessment(
            student_id=request.student_id,
            risk_score=risk_assessment['risk_score'],
            risk_level=risk_assessment['risk_level'],
            factors=risk_assessment['factors']
        )
        db.add(assessment)
        db.commit()
        
        return {
            "student_id": request.student_id,
            "risk_assessment": risk_assessment,
            "assessment_id": assessment.id
        }
    except Exception as e:
        logger.error(f"Error calculating risk: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/risk-scores")
async def get_risk_scores(
    school_id: Optional[int] = None,
    risk_level: Optional[str] = None,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get risk scores with filters."""
    try:
        query = db.query(RiskAssessment).join(Student)
        
        if school_id:
            query = query.filter(Student.school_id == school_id)
        
        if risk_level:
            query = query.filter(RiskAssessment.risk_level == risk_level)
        
        assessments = query.order_by(
            RiskAssessment.risk_score.desc()
        ).limit(limit).all()
        
        return {
            "assessments": [
                {
                    "id": a.id,
                    "student_id": a.student_id,
                    "risk_score": a.risk_score,
                    "risk_level": a.risk_level,
                    "factors": a.factors,
                    "calculated_at": a.calculated_at.isoformat() if a.calculated_at else None
                }
                for a in assessments
            ],
            "count": len(assessments)
        }
    except Exception as e:
        logger.error(f"Error getting risk scores: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/dashboard")
async def get_dashboard(
    school_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Get dashboard summary data."""
    try:
        # Get student counts
        student_query = db.query(Student)
        if school_id:
            student_query = student_query.filter(Student.school_id == school_id)
        
        total_students = student_query.count()
        at_risk_students = student_query.filter(Student.status == "at_risk").count()
        
        # Get risk distribution
        risk_query = db.query(RiskAssessment).join(Student)
        if school_id:
            risk_query = risk_query.filter(Student.school_id == school_id)
        
        risk_distribution = {
            "low": risk_query.filter(RiskAssessment.risk_level == "low").count(),
            "medium": risk_query.filter(RiskAssessment.risk_level == "medium").count(),
            "high": risk_query.filter(RiskAssessment.risk_level == "high").count(),
            "critical": risk_query.filter(RiskAssessment.risk_level == "critical").count()
        }
        
        return {
            "total_students": total_students,
            "at_risk_students": at_risk_students,
            "risk_distribution": risk_distribution,
            "at_risk_percentage": round((at_risk_students / total_students * 100) if total_students > 0 else 0, 2)
        }
    except Exception as e:
        logger.error(f"Error getting dashboard data: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


class BatchProcessRequest(BaseModel):
    """Request model for batch processing."""
    student_ids: List[int]


@router.post("/batch-process")
async def batch_process(
    request: BatchProcessRequest,
    db: Session = Depends(get_db)
):
    """Process multiple students for risk assessment."""
    try:
        results = []
        for student_id in request.student_ids:
            try:
                risk_assessment = risk_analyzer.calculate_risk_score(db, student_id)
                
                assessment = RiskAssessment(
                    student_id=student_id,
                    risk_score=risk_assessment['risk_score'],
                    risk_level=risk_assessment['risk_level'],
                    factors=risk_assessment['factors']
                )
                db.add(assessment)
                results.append({
                    "student_id": student_id,
                    "status": "success",
                    "risk_score": risk_assessment['risk_score'],
                    "risk_level": risk_assessment['risk_level']
                })
            except Exception as e:
                results.append({
                    "student_id": student_id,
                    "status": "error",
                    "error": str(e)
                })
        
        db.commit()
        
        return {
            "processed": len(results),
            "results": results
        }
    except Exception as e:
        logger.error(f"Error in batch process: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
