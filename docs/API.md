# API Documentation

## Base URL
`http://localhost:8000/api`

## Authentication
Currently, the API does not require authentication. In production, implement proper authentication.

## Endpoints

### Chat Endpoints

#### Start Conversation
```
POST /api/chat/start
Body: { "student_id": 1 } (optional)
Response: { "session_id": "uuid", "status": "started" }
```

#### Send Message
```
POST /api/chat/message
Body: {
    "session_id": "uuid",
    "message": "I need help with fees",
    "student_id": 1 (optional)
}
Response: {
    "session_id": "uuid",
    "response": "AI response text",
    "recommendations": [...],
    "problem_category": "financial",
    "severity": "medium",
    "escalated": false
}
```

### Analytics Endpoints

#### Upload Data
```
POST /api/analytics/upload-data
Content-Type: multipart/form-data
Body: file (CSV/Excel)
Response: {
    "status": "success",
    "processed": 10,
    "errors": []
}
```

#### Get Dashboard
```
GET /api/analytics/dashboard?school_id=1
Response: {
    "total_students": 100,
    "at_risk_students": 15,
    "risk_distribution": {...}
}
```

#### Get Risk Scores
```
GET /api/analytics/risk-scores?school_id=1&risk_level=high
Response: {
    "assessments": [...],
    "count": 5
}
```

### Student Endpoints

#### List Students
```
GET /api/students?school_id=1&status=at_risk
Response: {
    "students": [...],
    "total": 50
}
```

#### Get Student
```
GET /api/students/{id}
Response: { student details }
```

### Resource Endpoints

#### List Resources
```
GET /api/resources?category=financial&location=Mumbai
Response: {
    "resources": [...],
    "count": 10
}
```

For complete API documentation, visit `/docs` when the server is running.
