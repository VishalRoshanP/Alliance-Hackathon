"""Intervention tracking API endpoints."""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy.orm import Session
from datetime import datetime

from models.database import get_db
from models.intervention import Intervention
from utils.logger import setup_logger

logger = setup_logger()

router = APIRouter()


class InterventionCreate(BaseModel):
    """Intervention creation model."""
    student_id: int
    risk_assessment_id: Optional[int] = None
    type: str
    recommended_resources: Optional[List[int]] = None
    action_plan: Optional[str] = None
    assigned_to: Optional[int] = None


class InterventionUpdate(BaseModel):
    """Intervention update model."""
    status: Optional[str] = None
    action_plan: Optional[str] = None
    assigned_to: Optional[int] = None
    outcome: Optional[str] = None


@router.get("")
async def list_interventions(
    student_id: Optional[int] = None,
    status: Optional[str] = None,
    limit: int = 100,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """List interventions with filters."""
    try:
        query = db.query(Intervention)
        
        if student_id:
            query = query.filter(Intervention.student_id == student_id)
        
        if status:
            query = query.filter(Intervention.status == status)
        
        total = query.count()
        interventions = query.order_by(
            Intervention.created_at.desc()
        ).offset(offset).limit(limit).all()
        
        return {
            "interventions": [
                {
                    "id": i.id,
                    "student_id": i.student_id,
                    "type": i.type,
                    "status": i.status,
                    "action_plan": i.action_plan,
                    "assigned_to": i.assigned_to,
                    "created_at": i.created_at.isoformat() if i.created_at else None
                }
                for i in interventions
            ],
            "total": total,
            "limit": limit,
            "offset": offset
        }
    except Exception as e:
        logger.error(f"Error listing interventions: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{intervention_id}")
async def get_intervention(
    intervention_id: int,
    db: Session = Depends(get_db)
):
    """Get intervention details."""
    try:
        intervention = db.query(Intervention).filter(
            Intervention.id == intervention_id
        ).first()
        
        if not intervention:
            raise HTTPException(status_code=404, detail="Intervention not found")
        
        return {
            "id": intervention.id,
            "student_id": intervention.student_id,
            "risk_assessment_id": intervention.risk_assessment_id,
            "type": intervention.type,
            "status": intervention.status,
            "recommended_resources": intervention.recommended_resources,
            "action_plan": intervention.action_plan,
            "assigned_to": intervention.assigned_to,
            "started_at": intervention.started_at.isoformat() if intervention.started_at else None,
            "completed_at": intervention.completed_at.isoformat() if intervention.completed_at else None,
            "outcome": intervention.outcome,
            "created_at": intervention.created_at.isoformat() if intervention.created_at else None
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting intervention: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("")
async def create_intervention(
    intervention_data: InterventionCreate,
    db: Session = Depends(get_db)
):
    """Create a new intervention."""
    try:
        # Verify student exists
        from models.student import Student
        student = db.query(Student).filter(
            Student.id == intervention_data.student_id
        ).first()
        
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        
        intervention = Intervention(
            student_id=intervention_data.student_id,
            risk_assessment_id=intervention_data.risk_assessment_id,
            type=intervention_data.type,
            recommended_resources=intervention_data.recommended_resources or [],
            action_plan=intervention_data.action_plan,
            assigned_to=intervention_data.assigned_to,
            status="pending"
        )
        
        db.add(intervention)
        db.commit()
        db.refresh(intervention)
        
        return {
            "id": intervention.id,
            "student_id": intervention.student_id,
            "type": intervention.type,
            "status": "created"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating intervention: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{intervention_id}")
async def update_intervention(
    intervention_id: int,
    intervention_data: InterventionUpdate,
    db: Session = Depends(get_db)
):
    """Update intervention information."""
    try:
        intervention = db.query(Intervention).filter(
            Intervention.id == intervention_id
        ).first()
        
        if not intervention:
            raise HTTPException(status_code=404, detail="Intervention not found")
        
        # Update fields
        update_data = intervention_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(intervention, field, value)
        
        # Update timestamps based on status
        if intervention_data.status == "in_progress" and not intervention.started_at:
            intervention.started_at = datetime.now()
        elif intervention_data.status == "completed" and not intervention.completed_at:
            intervention.completed_at = datetime.now()
        
        db.commit()
        db.refresh(intervention)
        
        return {
            "id": intervention.id,
            "status": intervention.status,
            "updated": True
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating intervention: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/student/{student_id}")
async def get_student_interventions(
    student_id: int,
    db: Session = Depends(get_db)
):
    """Get all interventions for a student."""
    try:
        interventions = db.query(Intervention).filter(
            Intervention.student_id == student_id
        ).order_by(Intervention.created_at.desc()).all()
        
        return {
            "student_id": student_id,
            "interventions": [
                {
                    "id": i.id,
                    "type": i.type,
                    "status": i.status,
                    "action_plan": i.action_plan,
                    "created_at": i.created_at.isoformat() if i.created_at else None,
                    "completed_at": i.completed_at.isoformat() if i.completed_at else None
                }
                for i in interventions
            ],
            "count": len(interventions)
        }
    except Exception as e:
        logger.error(f"Error getting student interventions: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{intervention_id}/complete")
async def complete_intervention(
    intervention_id: int,
    outcome: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Mark intervention as completed."""
    try:
        intervention = db.query(Intervention).filter(
            Intervention.id == intervention_id
        ).first()
        
        if not intervention:
            raise HTTPException(status_code=404, detail="Intervention not found")
        
        intervention.status = "completed"
        intervention.completed_at = datetime.now()
        if outcome:
            intervention.outcome = outcome
        
        db.commit()
        
        return {
            "id": intervention.id,
            "status": "completed",
            "completed_at": intervention.completed_at.isoformat()
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error completing intervention: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
