"""LLM API integration service."""
import json
from typing import List, Dict, Optional
from openai import OpenAI
from groq import Groq
from config import settings
from utils.logger import setup_logger

logger = setup_logger()


class LLMService:
    """Service for interacting with LLM APIs."""
    
    def __init__(self):
        """Initialize LLM client based on provider."""
        self.provider = settings.LLM_PROVIDER.lower()
        self.client = None
        
        if self.provider == "openai":
            if not settings.OPENAI_API_KEY:
                raise ValueError("OPENAI_API_KEY not set")
            self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        elif self.provider == "groq":
            if not settings.GROQ_API_KEY:
                raise ValueError("GROQ_API_KEY not set")
            self.client = Groq(api_key=settings.GROQ_API_KEY)
        elif self.provider == "ollama":
            # Ollama uses OpenAI-compatible API
            self.client = OpenAI(
                base_url=settings.OLLAMA_BASE_URL,
                api_key="ollama"  # Ollama doesn't require real API key
            )
        else:
            raise ValueError(f"Unsupported LLM provider: {self.provider}")
    
    async def chat_completion(
        self,
        messages: List[Dict[str, str]],
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> str:
        """Get chat completion from LLM."""
        try:
            # Prepare messages
            formatted_messages = []
            if system_prompt:
                formatted_messages.append({"role": "system", "content": system_prompt})
            formatted_messages.extend(messages)
            
            # Call appropriate API
            if self.provider == "groq":
                response = self.client.chat.completions.create(
                    model="llama-3.1-70b-versatile",
                    messages=formatted_messages,
                    temperature=temperature,
                    max_tokens=max_tokens
                )
            elif self.provider == "openai":
                response = self.client.chat.completions.create(
                    model="gpt-4",
                    messages=formatted_messages,
                    temperature=temperature,
                    max_tokens=max_tokens
                )
            else:  # Ollama
                response = self.client.chat.completions.create(
                    model="llama2",
                    messages=formatted_messages,
                    temperature=temperature,
                    max_tokens=max_tokens
                )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Error in LLM chat completion: {str(e)}")
            raise
    
    async def analyze_text(
        self,
        text: str,
        task: str = "sentiment_analysis"
    ) -> Dict:
        """Analyze text for various tasks."""
        prompts = {
            "sentiment_analysis": "Analyze the sentiment of this text. Return JSON with 'sentiment' (positive/neutral/negative) and 'confidence' (0-1).",
            "problem_extraction": "Extract the main problem from this text. Return JSON with 'problem_category' (financial/family/health/academic/social/other), 'description', and 'severity' (low/medium/high/critical).",
            "summarize": "Summarize this text in 2-3 sentences.",
        }
        
        prompt = prompts.get(task, prompts["summarize"])
        
        messages = [
            {"role": "user", "content": f"{prompt}\n\nText: {text}"}
        ]
        
        response = await self.chat_completion(
            messages,
            system_prompt="You are a helpful assistant. Always return valid JSON.",
            temperature=0.3
        )
        
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            logger.warning(f"Failed to parse JSON response: {response}")
            return {"error": "Failed to parse response"}


# Global instance
llm_service = LLMService()
