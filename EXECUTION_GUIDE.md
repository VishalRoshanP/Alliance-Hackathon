# Execution Guide - Women's Education Dropout Prevention System

## Step-by-Step Execution Instructions

### Prerequisites
- Python 3.9 or higher installed
- pip package manager
- Internet connection (for downloading packages and API calls)

---

## Step 1: Setup Environment

### 1.1 Navigate to Project Directory
```bash
cd "women-education-system"
```

### 1.2 Create Virtual Environment (Recommended)
**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 1.3 Install Dependencies
```bash
pip install -r requirements.txt
```

**Note:** If you encounter errors, try:
```bash
pip install --upgrade pip
pip install -r requirements.txt --no-cache-dir
```

---

## Step 2: Configure Environment Variables

### 2.1 Create .env File
```bash
# Windows
copy .env.example .env

# Linux/Mac
cp .env.example .env
```

### 2.2 Edit .env File
Open `.env` in a text editor and configure:

**Minimum Required Configuration:**
```env
# LLM Configuration (Choose one provider)
LLM_PROVIDER=groq
GROQ_API_KEY=your_groq_api_key_here

# OR use OpenAI
# LLM_PROVIDER=openai
# OPENAI_API_KEY=your_openai_api_key_here

# OR use Ollama (local)
# LLM_PROVIDER=ollama
# OLLAMA_BASE_URL=http://localhost:11434
```

**Getting API Keys:**
- **Groq**: Sign up at https://console.groq.com (free tier available)
- **OpenAI**: Sign up at https://platform.openai.com
- **Ollama**: Install locally from https://ollama.ai

**Optional Configuration:**
- Database URL (defaults to SQLite)
- Email/SMS settings (for notifications)
- Other settings can use defaults

---

## Step 3: Initialize Database

### 3.1 Create Required Directories
```bash
# Windows
mkdir logs
mkdir uploads
mkdir backups

# Linux/Mac
mkdir -p logs uploads backups
```

### 3.2 Seed Database
```bash
python scripts/seed_database.py
```

**Expected Output:**
```
Initializing database...
Seeding data...
Seeded 2 schools
Seeded 1 resources
Database seeded successfully!
```

---

## Step 4: Run the Application

### 4.1 Start the Server
```bash
python main.py
```

**Expected Output:**
```
INFO:     Started server process
INFO:     Waiting for application startup.
Database initialized successfully
Application started successfully
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### 4.2 Verify Server is Running
Open your browser and visit:
- **API Root**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Frontend Dashboard**: http://localhost:8000/static/index.html
- **Chat Interface**: http://localhost:8000/static/chat.html
- **Analytics Dashboard**: http://localhost:8000/static/analytics.html

---

## Step 5: Test the System

### 5.1 Test Chat API
**Using Browser:**
1. Go to http://localhost:8000/static/chat.html
2. Type a message like: "I'm having trouble paying my fees"
3. Click Send
4. You should receive an AI response with recommendations

**Using curl (Command Line):**
```bash
# Start a conversation
curl -X POST http://localhost:8000/api/chat/start

# Send a message (replace SESSION_ID with actual session ID from above)
curl -X POST http://localhost:8000/api/chat/message \
  -H "Content-Type: application/json" \
  -d '{"session_id": "SESSION_ID", "message": "I need help with fees"}'
```

### 5.2 Test Analytics API
**Upload Sample Data:**
1. Create a CSV file `sample_students.csv`:
```csv
student_id,name,email,fees_pending,attendance_%
ST001,Anita Sharma,anita@example.com,25000,45
ST002,Priya Patel,priya@example.com,0,85
```

2. Go to http://localhost:8000/static/analytics.html
3. Click "Choose File" and select your CSV
4. Click "Upload Student Data"
5. View risk scores in the table

**Using API:**
```bash
curl -X POST http://localhost:8000/api/analytics/upload-data \
  -F "file=@sample_students.csv"
```

### 5.3 Test Risk Calculation
```bash
# Calculate risk for student ID 1
curl -X POST http://localhost:8000/api/analytics/calculate-risk \
  -H "Content-Type: application/json" \
  -d '{"student_id": 1}'
```

---

## Step 6: Common Operations

### 6.1 View API Documentation
Visit http://localhost:8000/docs for interactive API documentation (Swagger UI)

### 6.2 Check Logs
```bash
# Windows
type logs\app.log

# Linux/Mac
cat logs/app.log
```

### 6.3 Backup Database
```bash
python scripts/backup_database.py
```

### 6.4 Import Resources
```bash
python scripts/import_resources.py data/knowledge_base/scholarships.json
```

### 6.5 Export Data
```bash
# Export students
python scripts/export_data.py students students_export.csv

# Export risk assessments
python scripts/export_data.py risk risk_export.csv
```

---

## Troubleshooting

### Issue: "Module not found" errors
**Solution:**
```bash
pip install -r requirements.txt
```

### Issue: "Database locked" error
**Solution:** Close any other processes using the database, or restart the server

### Issue: "API key not found" error
**Solution:** 
1. Check your `.env` file exists
2. Verify API key is correctly set
3. Restart the server after changing `.env`

### Issue: Port 8000 already in use
**Solution:**
1. Change PORT in `.env` file
2. Or stop the process using port 8000:
   ```bash
   # Windows
   netstat -ano | findstr :8000
   taskkill /PID <PID> /F
   
   # Linux/Mac
   lsof -ti:8000 | xargs kill
   ```

### Issue: LLM API errors
**Solution:**
1. Verify API key is correct
2. Check API quota/limits
3. Try a different LLM provider
4. For Ollama, ensure it's running: `ollama serve`

### Issue: Frontend not loading
**Solution:**
1. Check server is running
2. Verify static files exist in `static/` directory
3. Check browser console for errors
4. Try accessing API directly: http://localhost:8000/api/health

---

## Production Deployment

### Using Gunicorn (Recommended for Production)
```bash
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Using Docker
```bash
# Build image
docker build -t women-education-system .

# Run container
docker run -p 8000:8000 --env-file .env women-education-system
```

---

## Next Steps

1. **Add More Resources**: Edit `data/knowledge_base/` JSON files
2. **Customize AI Responses**: Edit `core/chatbot.py` SYSTEM_PROMPT
3. **Adjust Risk Scoring**: Modify `core/risk_analyzer.py`
4. **Add Authentication**: Implement user authentication (not included)
5. **Deploy**: Follow deployment guide in `docs/DEPLOYMENT.md`

---

## Support

- **API Documentation**: http://localhost:8000/docs
- **Architecture Docs**: See `docs/ARCHITECTURE.md`
- **API Reference**: See `docs/API.md`

---

## Quick Reference Commands

```bash
# Start server
python main.py

# Seed database
python scripts/seed_database.py

# Backup database
python scripts/backup_database.py

# Run tests
pytest tests/

# Check health
curl http://localhost:8000/health
```

---

**Congratulations!** Your Women's Education Dropout Prevention System is now running! 🎉
