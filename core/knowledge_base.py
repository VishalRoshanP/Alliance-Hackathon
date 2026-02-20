"""Knowledge base search and management."""
from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from models.resource import Resource
from utils.constants import RESOURCE_TYPES
from utils.logger import setup_logger

logger = setup_logger()


class KnowledgeBase:
    """Knowledge base for resources and solutions."""
    
    @staticmethod
    def search_resources(
        db: Session,
        category: Optional[str] = None,
        resource_type: Optional[str] = None,
        location: Optional[str] = None,
        tags: Optional[List[str]] = None,
        limit: int = 10
    ) -> List[Resource]:
        """Search resources in knowledge base."""
        try:
            query = db.query(Resource).filter(Resource.availability == "available")
            
            if category:
                query = query.filter(Resource.category == category)
            
            if resource_type:
                query = query.filter(Resource.type == resource_type)
            
            if location:
                query = query.filter(Resource.location.contains(location))
            
            if tags:
                # Search in tags JSON field
                for tag in tags:
                    query = query.filter(Resource.tags.contains([tag]))
            
            return query.limit(limit).all()
        except Exception as e:
            logger.error(f"Error searching resources: {str(e)}")
            return []
    
    @staticmethod
    def get_resource_by_id(db: Session, resource_id: int) -> Optional[Resource]:
        """Get resource by ID."""
        try:
            return db.query(Resource).filter(Resource.id == resource_id).first()
        except Exception as e:
            logger.error(f"Error getting resource: {str(e)}")
            return None
    
    @staticmethod
    def get_resources_by_category(
        db: Session,
        category: str,
        limit: int = 5
    ) -> List[Resource]:
        """Get resources by category."""
        return KnowledgeBase.search_resources(
            db,
            category=category,
            limit=limit
        )
    
    @staticmethod
    def filter_by_eligibility(
        resources: List[Resource],
        student_data: Dict
    ) -> List[Resource]:
        """Filter resources by student eligibility."""
        # This is a simplified version
        # In production, you'd parse eligibility_criteria and match against student_data
        eligible_resources = []
        
        for resource in resources:
            # Basic filtering - can be enhanced
            if resource.availability == "available":
                eligible_resources.append(resource)
        
        return eligible_resources


# Global instance
knowledge_base = KnowledgeBase()
