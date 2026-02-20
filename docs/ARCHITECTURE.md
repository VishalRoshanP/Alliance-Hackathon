# Architecture Documentation

## System Architecture

The Women's Education Dropout Prevention System is built using:

- **Backend**: FastAPI (Python)
- **Database**: SQLite (dev) / PostgreSQL (prod)
- **AI**: LLM integration (Groq/OpenAI/Ollama)
- **Frontend**: Vanilla JavaScript, HTML, CSS

## Component Overview

### 1. API Layer (`api/`)
- RESTful endpoints for all operations
- Request validation using Pydantic
- Error handling and logging

### 2. Core Business Logic (`core/`)
- **Chatbot**: AI conversation engine
- **Risk Analyzer**: Dropout risk calculation
- **Solution Engine**: Resource recommendation
- **NLP Processor**: Text analysis
- **Knowledge Base**: Resource search

### 3. Data Layer (`models/`)
- SQLAlchemy ORM models
- Database schema definitions
- Relationships between entities

### 4. Service Layer (`services/`)
- LLM API integration
- Notification services (Email/SMS)
- File upload handling
- Data export

### 5. Frontend (`static/`)
- Dashboard for analytics
- Chat interface
- Data upload interface

## Data Flow

1. **Student Chat Flow**:
   Student → Chat API → NLP Processor → LLM Service → Solution Engine → Response

2. **Risk Analysis Flow**:
   School Data → Upload API → Risk Analyzer → Database → Dashboard

3. **Resource Recommendation Flow**:
   Problem → Solution Engine → Knowledge Base → Filtered Resources → Student

## Security Considerations

- Input validation on all endpoints
- SQL injection prevention (SQLAlchemy ORM)
- File upload size limits
- CORS configuration
- Environment variable management

## Scalability

- Stateless API design
- Database connection pooling
- Caching strategies (can be added)
- Horizontal scaling support
