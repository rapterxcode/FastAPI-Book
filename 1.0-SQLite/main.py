from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.config import settings
from app.database import lifespan
from app.api.health import router as health_router
from app.api.v1.endpoints.books import router as books_router

# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    description=settings.app_description,
    version=settings.app_version,
    lifespan=lifespan
)

# Include routers
app.include_router(health_router, tags=["health"])
app.include_router(books_router, prefix="/books", tags=["books"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=settings.port,
        reload=True
    )





