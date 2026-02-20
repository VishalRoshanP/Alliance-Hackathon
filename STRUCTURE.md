# Project Structure

This document describes the structure of the Women's Education Dropout Prevention System.

See `structure.txt` for the complete technical structure.

## Quick Reference

- **API Endpoints**: `/api/` - All REST API routes
- **Core Logic**: `/core/` - Business logic and AI engines
- **Database Models**: `/models/` - SQLAlchemy models
- **Services**: `/services/` - External service integrations
- **Frontend**: `/static/` - HTML, CSS, JavaScript files
- **Data**: `/data/` - Knowledge base and seed data
- **Scripts**: `/scripts/` - Utility scripts
- **Tests**: `/tests/` - Test files

## Key Components

1. **Chatbot** (`core/chatbot.py`) - AI chat engine
2. **Risk Analyzer** (`core/risk_analyzer.py`) - Risk scoring system
3. **Solution Engine** (`core/solution_engine.py`) - Resource recommendations
4. **LLM Service** (`services/llm_service.py`) - AI model integration
5. **Database** (`models/`) - All data models
