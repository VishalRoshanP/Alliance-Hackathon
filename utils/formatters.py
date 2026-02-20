"""Data formatting utilities."""
from datetime import datetime
from typing import Optional, Dict, Any


def format_date(date: Optional[datetime]) -> Optional[str]:
    """Format datetime to string."""
    if date is None:
        return None
    return date.strftime('%Y-%m-%d %H:%M:%S')


def format_currency(amount: float, currency: str = "₹") -> str:
    """Format currency amount."""
    return f"{currency}{amount:,.2f}"


def format_percentage(value: float, decimals: int = 2) -> str:
    """Format percentage."""
    return f"{value:.{decimals}f}%"


def format_risk_level(score: float) -> str:
    """Format risk level based on score."""
    if score < 30:
        return "Low"
    elif score < 60:
        return "Medium"
    elif score < 80:
        return "High"
    else:
        return "Critical"


def format_student_summary(student: Dict[str, Any]) -> str:
    """Format student summary."""
    return f"{student.get('name', 'Unknown')} (ID: {student.get('student_id', 'N/A')})"


def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate text to max length."""
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."


def format_file_size(size_bytes: int) -> str:
    """Format file size in human-readable format."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"
