from sqlmodel import SQLModel, create_engine, Session
from contextlib import asynccontextmanager
from config import DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
    pool_size=10,
    max_overflow=20
)

def get_session():
    with Session(engine) as session:
        yield session

@asynccontextmanager
async def lifespan(app=None):
    # SQLModel.metadata.create_all(engine)  # Uncomment if you want auto-create
    yield 