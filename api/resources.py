"""Resource management API endpoints."""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy.orm import Session

from models.database import get_db
from models.resource import Resource, ResourceRecommendation
from core.knowledge_base import knowledge_base
from utils.logger import setup_logger

logger = setup_logger()

router = APIRouter()


class ResourceCreate(BaseModel):
    """Resource creation model."""
    title: str
    type: str
    category: Optional[str] = None
    description: Optional[str] = None
    eligibility_criteria: Optional[str] = None
    application_process: Optional[str] = None
    contact_info: Optional[dict] = None
    location: Optional[str] = None
    availability: Optional[str] = "available"
    tags: Optional[List[str]] = None


class ResourceUpdate(BaseModel):
    """Resource update model."""
    title: Optional[str] = None
    type: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
    eligibility_criteria: Optional[str] = None
    application_process: Optional[str] = None
    contact_info: Optional[dict] = None
    location: Optional[str] = None
    availability: Optional[str] = None
    tags: Optional[List[str]] = None


@router.get("")
async def list_resources(
    category: Optional[str] = None,
    resource_type: Optional[str] = None,
    location: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """List resources with filters."""
    try:
        resources = knowledge_base.search_resources(
            db,
            category=category,
            resource_type=resource_type,
            location=location,
            limit=limit + offset
        )
        
        # Apply offset
        resources = resources[offset:offset+limit]
        
        return {
            "resources": [
                {
                    "id": r.id,
                    "title": r.title,
                    "type": r.type,
                    "category": r.category,
                    "description": r.description,
                    "location": r.location,
                    "availability": r.availability
                }
                for r in resources
            ],
            "count": len(resources)
        }
    except Exception as e:
        logger.error(f"Error listing resources: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{resource_id}")
async def get_resource(
    resource_id: int,
    db: Session = Depends(get_db)
):
    """Get resource details."""
    try:
        resource = knowledge_base.get_resource_by_id(db, resource_id)
        
        if not resource:
            raise HTTPException(status_code=404, detail="Resource not found")
        
        return {
            "id": resource.id,
            "title": resource.title,
            "type": resource.type,
            "category": resource.category,
            "description": resource.description,
            "eligibility_criteria": resource.eligibility_criteria,
            "application_process": resource.application_process,
            "contact_info": resource.contact_info,
            "location": resource.location,
            "availability": resource.availability,
            "tags": resource.tags
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting resource: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("")
async def create_resource(
    resource_data: ResourceCreate,
    db: Session = Depends(get_db)
):
    """Add a new resource."""
    try:
        resource = Resource(**resource_data.dict())
        db.add(resource)
        db.commit()
        db.refresh(resource)
        
        return {
            "id": resource.id,
            "title": resource.title,
            "status": "created"
        }
    except Exception as e:
        logger.error(f"Error creating resource: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{resource_id}")
async def update_resource(
    resource_id: int,
    resource_data: ResourceUpdate,
    db: Session = Depends(get_db)
):
    """Update resource information."""
    try:
        resource = knowledge_base.get_resource_by_id(db, resource_id)
        
        if not resource:
            raise HTTPException(status_code=404, detail="Resource not found")
        
        # Update fields
        update_data = resource_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(resource, field, value)
        
        db.commit()
        db.refresh(resource)
        
        return {
            "id": resource.id,
            "title": resource.title,
            "status": "updated"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating resource: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{resource_id}")
async def delete_resource(
    resource_id: int,
    db: Session = Depends(get_db)
):
    """Delete a resource."""
    try:
        resource = knowledge_base.get_resource_by_id(db, resource_id)
        
        if not resource:
            raise HTTPException(status_code=404, detail="Resource not found")
        
        db.delete(resource)
        db.commit()
        
        return {"status": "deleted", "resource_id": resource_id}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting resource: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/search")
async def search_resources(
    query: str,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """Search resources by query."""
    try:
        # Simple search - can be enhanced with full-text search
        resources = db.query(Resource).filter(
            (Resource.title.contains(query)) |
            (Resource.description.contains(query)) |
            (Resource.category.contains(query))
        ).limit(limit).all()
        
        return {
            "query": query,
            "resources": [
                {
                    "id": r.id,
                    "title": r.title,
                    "type": r.type,
                    "category": r.category,
                    "description": r.description[:200] if r.description else None
                }
                for r in resources
            ],
            "count": len(resources)
        }
    except Exception as e:
        logger.error(f"Error searching resources: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/recommend/{student_id}")
async def recommend_resources(
    student_id: int,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Get resource recommendations for a student."""
    try:
        from models.student import Student
        
        student = db.query(Student).filter(Student.id == student_id).first()
        
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        
        # Get recommendations from database
        recommendations = db.query(ResourceRecommendation).filter(
            ResourceRecommendation.student_id == student_id
        ).order_by(ResourceRecommendation.recommended_at.desc()).limit(limit).all()
        
        resources = []
        for rec in recommendations:
            resource = knowledge_base.get_resource_by_id(db, rec.resource_id)
            if resource:
                resources.append({
                    "id": resource.id,
                    "title": resource.title,
                    "type": resource.type,
                    "description": resource.description,
                    "recommended_at": rec.recommended_at.isoformat() if rec.recommended_at else None,
                    "student_viewed": rec.student_viewed,
                    "student_applied": rec.student_applied
                })
        
        return {
            "student_id": student_id,
            "resources": resources,
            "count": len(resources)
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting recommendations: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
