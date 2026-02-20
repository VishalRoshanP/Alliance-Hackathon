"""NLP processor for understanding student messages."""
from typing import Dict, Optional
from services.llm_service import llm_service
from utils.constants import PROBLEM_CATEGORIES, SENTIMENT_POSITIVE, SENTIMENT_NEUTRAL, SENTIMENT_NEGATIVE
from utils.logger import setup_logger

logger = setup_logger()


class NLPProcessor:
    """Processes natural language to extract meaning."""
    
    @staticmethod
    async def understand_problem(message: str) -> Dict:
        """Understand the problem from student message."""
        try:
            # Use LLM to analyze the message
            analysis = await llm_service.analyze_text(message, task="problem_extraction")
            
            # Extract key information
            problem_category = analysis.get("problem_category", "other")
            description = analysis.get("description", message)
            severity = analysis.get("severity", "medium")
            
            # Extract additional details using LLM
            details_prompt = f"""Extract key details from this message: "{message}"
            
            Return JSON with:
            - amount (if financial issue, extract number)
            - location (if mentioned)
            - urgency (true/false)
            - keywords (array of important words)
            """
            
            details_response = await llm_service.chat_completion(
                [{"role": "user", "content": details_prompt}],
                system_prompt="Return only valid JSON.",
                temperature=0.3
            )
            
            try:
                import json
                details = json.loads(details_response)
            except:
                details = {}
            
            return {
                "problem_category": problem_category,
                "description": description,
                "severity": severity,
                "amount": details.get("amount"),
                "location": details.get("location"),
                "urgency": details.get("urgency", False),
                "keywords": details.get("keywords", [])
            }
        except Exception as e:
            logger.error(f"Error understanding problem: {str(e)}")
            return {
                "problem_category": "other",
                "description": message,
                "severity": "medium"
            }
    
    @staticmethod
    async def analyze_sentiment(message: str) -> str:
        """Analyze sentiment of message."""
        try:
            analysis = await llm_service.analyze_text(message, task="sentiment_analysis")
            sentiment = analysis.get("sentiment", SENTIMENT_NEUTRAL).lower()
            
            if sentiment not in [SENTIMENT_POSITIVE, SENTIMENT_NEUTRAL, SENTIMENT_NEGATIVE]:
                return SENTIMENT_NEUTRAL
            return sentiment
        except Exception as e:
            logger.error(f"Error analyzing sentiment: {str(e)}")
            return SENTIMENT_NEUTRAL
    
    @staticmethod
    async def extract_keywords(message: str) -> list:
        """Extract keywords from message."""
        try:
            prompt = f"""Extract important keywords from this message: "{message}"
            
            Return JSON array of keywords (max 10).
            """
            
            response = await llm_service.chat_completion(
                [{"role": "user", "content": prompt}],
                system_prompt="Return only valid JSON array.",
                temperature=0.3
            )
            
            import json
            keywords = json.loads(response)
            return keywords if isinstance(keywords, list) else []
        except Exception as e:
            logger.error(f"Error extracting keywords: {str(e)}")
            return []


# Global instance
nlp_processor = NLPProcessor()
