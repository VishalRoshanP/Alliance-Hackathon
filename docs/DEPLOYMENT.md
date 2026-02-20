# Deployment Guide

## Prerequisites

- Python 3.9+
- pip
- Virtual environment (recommended)

## Local Development Setup

1. **Clone and navigate to project**
```bash
cd women-education-system
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate    # Windows
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment**
```bash
cp .env.example .env
# Edit .env and add your API keys
```

5. **Initialize database**
```bash
python scripts/seed_database.py
```

6. **Run the application**
```bash
python main.py
```

The API will be available at `http://localhost:8000`

## Production Deployment

### Using Docker (Recommended)

1. **Build Docker image**
```bash
docker build -t women-education-system .
```

2. **Run container**
```bash
docker run -p 8000:8000 --env-file .env women-education-system
```

### Using Gunicorn

```bash
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Environment Variables

Set these in production:
- `DATABASE_URL` - PostgreSQL connection string
- `SECRET_KEY` - Strong secret key
- `LLM_PROVIDER` - groq, openai, or ollama
- API keys for chosen LLM provider
- Email/SMS credentials if using notifications

## Database Migration

For production, use PostgreSQL:

1. Update `DATABASE_URL` in `.env`
2. Run migrations (if using Alembic)
3. Seed initial data: `python scripts/seed_database.py`

## Monitoring

- Check logs in `logs/app.log`
- Monitor API endpoints at `/health`
- Use `/docs` for API documentation
