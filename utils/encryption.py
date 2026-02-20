"""Data encryption utilities."""
import hashlib
from passlib.context import CryptContext
from config import settings

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a password."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)


def hash_string(text: str) -> str:
    """Create a hash of a string."""
    return hashlib.sha256(text.encode()).hexdigest()


def create_session_id() -> str:
    """Create a unique session ID."""
    import uuid
    return str(uuid.uuid4())
