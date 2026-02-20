"""Chatbot API endpoints."""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.orm import Session

from models.database import get_db
from core.chatbot import chatbot
from utils.logger import setup_logger

logger = setup_logger()

router = APIRouter()


class ChatMessageRequest(BaseModel):
    """Request model for chat message."""
    session_id: Optional[str] = None
    message: str
    student_id: Optional[int] = None


class ChatMessageResponse(BaseModel):
    """Response model for chat message."""
    session_id: str
    response: str
    recommendations: list
    problem_category: Optional[str] = None
    severity: Optional[str] = None
    escalated: bool = False


@router.post("/start", response_model=dict)
async def start_conversation(
    student_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Start a new conversation."""
    try:
        session_id = await chatbot.start_conversation(db, student_id)
        return {"session_id": session_id, "status": "started"}
    except Exception as e:
        logger.error(f"Error starting conversation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/message", response_model=ChatMessageResponse)
async def send_message(
    request: ChatMessageRequest,
    db: Session = Depends(get_db)
):
    """Send a message and get AI response."""
    try:
        # Start conversation if no session_id provided
        if not request.session_id:
            request.session_id = await chatbot.start_conversation(db, request.student_id)
        
        result = await chatbot.process_message(
            db,
            request.session_id,
            request.message,
            request.student_id
        )
        
        return ChatMessageResponse(
            session_id=request.session_id,
            response=result["response"],
            recommendations=result.get("recommendations", []),
            problem_category=result.get("problem_category"),
            severity=result.get("severity"),
            escalated=result.get("escalated", False)
        )
    except Exception as e:
        logger.error(f"Error processing message: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/conversations")
async def get_conversations(
    student_id: Optional[int] = None,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """Get list of conversations."""
    try:
        from models.conversation import Conversation
        
        query = db.query(Conversation)
        if student_id:
            query = query.filter(Conversation.student_id == student_id)
        
        conversations = query.order_by(Conversation.created_at.desc()).limit(limit).all()
        
        return {
            "conversations": [
                {
                    "id": conv.id,
                    "session_id": conv.session_id,
                    "student_id": conv.student_id,
                    "status": conv.status,
                    "started_at": conv.started_at.isoformat() if conv.started_at else None,
                    "message_count": len(conv.messages)
                }
                for conv in conversations
            ]
        }
    except Exception as e:
        logger.error(f"Error getting conversations: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/conversations/{session_id}")
async def get_conversation(
    session_id: str,
    db: Session = Depends(get_db)
):
    """Get conversation history."""
    try:
        from models.conversation import Conversation, Message
        
        conversation = db.query(Conversation).filter(
            Conversation.session_id == session_id
        ).first()
        
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        messages = db.query(Message).filter(
            Message.conversation_id == conversation.id
        ).order_by(Message.created_at.asc()).all()
        
        return {
            "conversation": {
                "id": conversation.id,
                "session_id": conversation.session_id,
                "student_id": conversation.student_id,
                "status": conversation.status,
                "started_at": conversation.started_at.isoformat() if conversation.started_at else None,
                "messages": [
                    {
                        "role": msg.role,
                        "content": msg.content,
                        "created_at": msg.created_at.isoformat() if msg.created_at else None,
                        "problem_category": msg.problem_category,
                        "severity": msg.severity
                    }
                    for msg in messages
                ]
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting conversation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/escalate")
async def escalate_conversation(
    session_id: str,
    db: Session = Depends(get_db)
):
    """Escalate conversation to human counselor."""
    try:
        from models.conversation import Conversation
        
        conversation = db.query(Conversation).filter(
            Conversation.session_id == session_id
        ).first()
        
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        conversation.status = "escalated"
        db.commit()
        
        # TODO: Send notification to counselors
        
        return {"status": "escalated", "message": "Conversation escalated to human counselor"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error escalating conversation: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
