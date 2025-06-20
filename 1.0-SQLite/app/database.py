from sqlmodel import SQLModel, create_engine, Session
from contextlib import asynccontextmanager
from .config import settings

# Create database engine
engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False}
)

def create_db_and_tables():
    """Create database and tables"""
    SQLModel.metadata.create_all(engine)

def get_session():
    """Dependency to get database session"""
    with Session(engine) as session:
        yield session

@asynccontextmanager
async def lifespan():
    """Application lifespan manager"""
    create_db_and_tables()
    yield 