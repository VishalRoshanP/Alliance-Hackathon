"""FastAPI application entry point."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from api import chat, analytics, students, schools, resources, interventions
from models.database import init_db
from config import settings
from utils.logger import setup_logger

# Setup logger
logger = setup_logger()

# Create FastAPI app
app = FastAPI(
    title="Women's Education Dropout Prevention System",
    description="AI-powered system to prevent women's education dropout",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat.router, prefix="/api/chat", tags=["chat"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["analytics"])
app.include_router(students.router, prefix="/api/students", tags=["students"])
app.include_router(schools.router, prefix="/api/schools", tags=["schools"])
app.include_router(resources.router, prefix="/api/resources", tags=["resources"])
app.include_router(interventions.router, prefix="/api/interventions", tags=["interventions"])

# Mount static files
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")


@app.on_event("startup")
async def startup():
    """Initialize database on startup."""
    try:
        init_db()
        logger.info("Database initialized successfully")
        
        # Create upload directory if it doesn't exist
        os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
        os.makedirs("logs", exist_ok=True)
        
        logger.info("Application started successfully")
    except Exception as e:
        logger.error(f"Error during startup: {str(e)}")
        raise


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Women's Education Dropout Prevention API",
        "version": "1.0.0",
        "docs": "/docs",
        "frontend": "/static/index.html"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
