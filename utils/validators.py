"""Data validation utilities."""
import re
from typing import Optional
from datetime import datetime


def validate_email(email: str) -> bool:
    """Validate email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_phone(phone: str) -> bool:
    """Validate phone number format."""
    # Remove spaces, dashes, and parentheses
    cleaned = re.sub(r'[\s\-\(\)]', '', phone)
    # Check if it's digits and reasonable length (10-15 digits)
    return cleaned.isdigit() and 10 <= len(cleaned) <= 15


def validate_student_id(student_id: str) -> bool:
    """Validate student ID format."""
    # Alphanumeric, 3-50 characters
    return bool(re.match(r'^[A-Za-z0-9_-]{3,50}$', student_id))


def validate_date(date_string: str) -> bool:
    """Validate date format (YYYY-MM-DD)."""
    try:
        datetime.strptime(date_string, '%Y-%m-%d')
        return True
    except ValueError:
        return False


def sanitize_input(text: str, max_length: int = 10000) -> str:
    """Sanitize user input."""
    if not text:
        return ""
    # Remove potentially dangerous characters
    text = text.strip()
    if len(text) > max_length:
        text = text[:max_length]
    return text


def validate_risk_score(score: float) -> bool:
    """Validate risk score is between 0 and 100."""
    return 0 <= score <= 100


def validate_percentage(value: float) -> bool:
    """Validate percentage is between 0 and 100."""
    return 0 <= value <= 100
