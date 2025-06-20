from fastapi import APIRouter
from datetime import datetime
from sqlmodel import Session, select
from ..database import engine
from ..models import Book
from ..config import settings

router = APIRouter()

@router.get("/")
def health_check():
    """Health check endpoint"""
    try:
        with Session(engine) as session:
            result = session.exec(select(Book).limit(1))
            db_status = "Connected"
            db_message = "Database connection successful"
    except Exception as e:
        db_status = "Error"
        db_message = f"Database connection failed: {str(e)}"
    
    return {
        "status": "healthy" if db_status == "Connected" else "unhealthy",
        "server": {
            "status": "Running",
            "timestamp": datetime.now().isoformat(),
            "framework": "FastAPI",
            "name": settings.app_name,
            "version": settings.app_version,
            "description": settings.app_description,
            "environment": settings.environment,
            "port": settings.port
        },
        "database": {
            "type": "SQLite",
            "status": db_status,
            "message": db_message,
            "database": settings.db_name
        },
        "endpoints": {
            "total": 8,
            "available": [
                "GET /",
                "GET /docs",
                "POST /books",
                "GET /books",
                "GET /books/search",
                "GET /books/{book_id}",
                "PUT /books/{book_id}",
                "DELETE /books/{book_id}"
            ]
        }
    } 