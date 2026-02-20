"""Solution recommendation engine."""
from typing import List, Dict
from sqlalchemy.orm import Session
from core.knowledge_base import knowledge_base
from utils.constants import PROBLEM_CATEGORIES
from utils.logger import setup_logger

logger = setup_logger()


class SolutionEngine:
    """Engine for recommending solutions."""
    
    @staticmethod
    def recommend_solutions(
        db: Session,
        problem: Dict,
        student_context: Dict = None
    ) -> List[Dict]:
        """Recommend solutions based on problem and student context."""
        try:
            category = problem.get("problem_category", "other")
            location = problem.get("location")
            
            # Map problem category to resource category
            category_mapping = {
                "financial": "financial",
                "family": "social",
                "health": "health",
                "academic": "academic",
                "social": "social",
                "other": None
            }
            
            resource_category = category_mapping.get(category)
            
            # Search resources
            resources = knowledge_base.search_resources(
                db,
                category=resource_category,
                location=location,
                limit=10
            )
            
            # Filter by eligibility if student context provided
            if student_context:
                resources = knowledge_base.filter_by_eligibility(
                    resources,
                    student_context
                )
            
            # Convert to dict format
            recommendations = []
            for resource in resources:
                recommendations.append({
                    "id": resource.id,
                    "title": resource.title,
                    "type": resource.type,
                    "description": resource.description,
                    "eligibility": resource.eligibility_criteria,
                    "application_process": resource.application_process,
                    "contact_info": resource.contact_info,
                    "location": resource.location
                })
            
            # Prioritize recommendations
            return SolutionEngine.prioritize_recommendations(recommendations, problem)
        except Exception as e:
            logger.error(f"Error recommending solutions: {str(e)}")
            return []
    
    @staticmethod
    def prioritize_recommendations(
        recommendations: List[Dict],
        problem: Dict
    ) -> List[Dict]:
        """Prioritize recommendations based on problem."""
        # Simple prioritization - can be enhanced
        # Prioritize by type matching problem category
        category = problem.get("problem_category", "other")
        
        type_priority = {
            "financial": ["scholarship", "program"],
            "health": ["health", "organization"],
            "academic": ["program", "organization"],
            "family": ["counseling", "organization"],
            "social": ["organization", "program"]
        }
        
        priority_types = type_priority.get(category, [])
        
        def get_priority(rec):
            rec_type = rec.get("type", "")
            if rec_type in priority_types:
                return priority_types.index(rec_type)
            return len(priority_types)
        
        return sorted(recommendations, key=get_priority)
    
    @staticmethod
    def generate_action_plan(solutions: List[Dict]) -> Dict:
        """Generate action plan from solutions."""
        if not solutions:
            return {
                "steps": [],
                "estimated_time": "N/A",
                "resources_needed": []
            }
        
        steps = []
        for idx, solution in enumerate(solutions[:5], 1):  # Top 5 solutions
            steps.append({
                "step": idx,
                "action": f"Apply for {solution.get('title', 'resource')}",
                "description": solution.get("application_process", "Contact the organization"),
                "resource_id": solution.get("id")
            })
        
        return {
            "steps": steps,
            "estimated_time": f"{len(steps) * 2} weeks",
            "resources_needed": [s.get("title") for s in solutions[:5]]
        }


# Global instance
solution_engine = SolutionEngine()
