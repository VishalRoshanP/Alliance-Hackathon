# Women's Education Dropout Prevention System

An AI-powered system to help prevent women's education dropout through intelligent chat support and proactive risk analysis.

## Features

- 🤖 **AI Chatbot**: 24/7 support for students facing educational challenges
- 📊 **Risk Analysis**: Automated risk scoring based on attendance, fees, health, and academic performance
- 📚 **Resource Database**: Comprehensive knowledge base of scholarships, programs, and support services
- 🎯 **Personalized Recommendations**: AI-powered solution matching based on student profile
- 📈 **Analytics Dashboard**: Real-time insights and trend analysis
- 🔔 **Intervention Tracking**: Monitor and track intervention outcomes

## Quick Start

### Prerequisites

- Python 3.9 or higher
- pip package manager

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd women-education-system
```

2. **Create virtual environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
copy .env.example .env
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
The frontend will be available at `http://localhost:8000/static/index.html`

## Configuration

Edit `.env` file to configure:
- LLM provider (Groq/OpenAI/Ollama)
- Database connection
- Email/SMS notifications
- File upload settings

## API Documentation

Once the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Project Structure

```
women-education-system/
├── api/              # API endpoints
├── core/             # Business logic
├── models/           # Database models
├── services/         # Service layer
├── utils/            # Utilities
├── static/           # Frontend files
├── data/             # Data files
├── scripts/          # Utility scripts
└── tests/            # Test files
```

## Usage Examples

### Chat with AI
```python
POST /api/chat/message
{
    "session_id": "abc123",
    "message": "I'm having trouble paying fees"
}
```

### Upload School Data
```python
POST /api/analytics/upload-data
Content-Type: multipart/form-data
file: students_data.csv
```

### Get Risk Scores
```python
GET /api/analytics/risk-scores?school_id=1&risk_level=high
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License

## Support

For issues and questions, please open an issue on GitHub.
