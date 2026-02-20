"""Chatbot AI engine."""
from typing import Dict, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime
import uuid

from services.llm_service import llm_service
from core.nlp_processor import nlp_processor
from core.solution_engine import solution_engine
from core.risk_analyzer import risk_analyzer
from core.knowledge_base import knowledge_base
from models.conversation import Conversation, Message
from models.student import Student
from utils.constants import RISK_CRITICAL, RISK_HIGH
from utils.logger import setup_logger

logger = setup_logger()


class Chatbot:
    """Chatbot engine for student interactions."""
    
    SYSTEM_PROMPT = """You are a helpful and empathetic AI assistant for a Women's Education Dropout Prevention System. 
    Your role is to:
    1. Listen empathetically to students' problems
    2. Understand their challenges (financial, family, health, academic, etc.)
    3. Provide helpful guidance and resources
    4. Be supportive and encouraging
    5. Escalate critical cases when needed
    
    Always be:
    - Kind and understanding
    - Clear and concise
    - Action-oriented (provide specific next steps)
    - Culturally sensitive
    
    Never:
    - Make promises you can't keep
    - Provide medical or legal advice
    - Be dismissive of their concerns
    """
    
    @staticmethod
    async def start_conversation(
        db: Session,
        student_id: Optional[int] = None
    ) -> str:
        """Start a new conversation and return session_id."""
        try:
            session_id = str(uuid.uuid4())
            
            conversation = Conversation(
                session_id=session_id,
                student_id=student_id,
                status="active"
            )
            
            db.add(conversation)
            db.commit()
            
            logger.info(f"Started conversation: {session_id}")
            return session_id
        except Exception as e:
            logger.error(f"Error starting conversation: {str(e)}")
            db.rollback()
            raise
    
    @staticmethod
    async def process_message(
        db: Session,
        session_id: str,
        message: str,
        student_id: Optional[int] = None
    ) -> Dict:
        """Process a message and generate response."""
        try:
            # Get or create conversation
            conversation = db.query(Conversation).filter(
                Conversation.session_id == session_id
            ).first()
            
            if not conversation:
                conversation = Conversation(
                    session_id=session_id,
                    student_id=student_id,
                    status="active"
                )
                db.add(conversation)
                db.commit()
                db.refresh(conversation)
            
            # Save user message
            user_message = Message(
                conversation_id=conversation.id,
                role="user",
                content=message
            )
            db.add(user_message)
            
            # Analyze message
            problem = await nlp_processor.understand_problem(message)
            sentiment = await nlp_processor.analyze_sentiment(message)
            
            # Update message with analysis
            user_message.problem_category = problem.get("problem_category")
            user_message.severity = problem.get("severity")
            user_message.sentiment = sentiment
            
            # Get student context if available
            student_context = {}
            if conversation.student_id:
                student = db.query(Student).filter(
                    Student.id == conversation.student_id
                ).first()
                if student:
                    student_context = {
                        "student_id": student.student_id,
                        "name": student.name,
                        "location": student.address,
                        "school_id": student.school_id
                    }
            
            # Get recommendations
            recommendations = solution_engine.recommend_solutions(
                db,
                problem,
                student_context
            )
            
            # Generate response using LLM
            context_messages = await Chatbot._get_conversation_history(db, conversation.id)
            
            response_prompt = f"""Student message: "{message}"

Problem identified: {problem.get('description', 'General inquiry')}
Category: {problem.get('problem_category', 'other')}
Severity: {problem.get('severity', 'medium')}

Available resources: {len(recommendations)} found

Provide a helpful, empathetic response that:
1. Acknowledges their concern
2. Offers specific resources if available
3. Provides clear next steps
4. Encourages them to continue their education

Keep response concise (2-3 paragraphs max).
"""
            
            if recommendations:
                response_prompt += f"\n\nTop resources to mention:\n"
                for rec in recommendations[:3]:
                    response_prompt += f"- {rec.get('title')}: {rec.get('description', '')[:100]}\n"
            
            ai_response = await llm_service.chat_completion(
                context_messages + [{"role": "user", "content": response_prompt}],
                system_prompt=Chatbot.SYSTEM_PROMPT,
                temperature=0.7
            )
            
            # Save assistant message
            assistant_message = Message(
                conversation_id=conversation.id,
                role="assistant",
                content=ai_response
            )
            db.add(assistant_message)
            
            # Check if escalation needed
            should_escalate = Chatbot._should_escalate(problem, conversation.student_id, db)
            
            if should_escalate:
                conversation.status = "escalated"
                # TODO: Send notification to counselors
            
            db.commit()
            
            return {
                "response": ai_response,
                "recommendations": recommendations[:5],
                "problem_category": problem.get("problem_category"),
                "severity": problem.get("severity"),
                "escalated": should_escalate
            }
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            db.rollback()
            raise
    
    @staticmethod
    async def _get_conversation_history(db: Session, conversation_id: int, limit: int = 10) -> list:
        """Get conversation history."""
        messages = db.query(Message).filter(
            Message.conversation_id == conversation_id
        ).order_by(Message.created_at.desc()).limit(limit).all()
        
        # Reverse to get chronological order
        messages.reverse()
        
        formatted_messages = []
        for msg in messages:
            formatted_messages.append({
                "role": msg.role,
                "content": msg.content
            })
        
        return formatted_messages
    
    @staticmethod
    def _should_escalate(problem: Dict, student_id: Optional[int], db: Session) -> bool:
        """Determine if case should be escalated."""
        # Escalate if:
        # 1. Critical severity
        # 2. High risk student
        # 3. Multiple high-severity issues
        
        if problem.get("severity") == "critical":
            return True
        
        if student_id:
            try:
                risk_assessment = risk_analyzer.calculate_risk_score(db, student_id)
                if risk_assessment['risk_level'] in [RISK_HIGH, RISK_CRITICAL]:
                    return True
            except:
                pass
        
        return False


# Global instance
chatbot = Chatbot()
