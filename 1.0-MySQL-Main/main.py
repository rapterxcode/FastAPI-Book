from typing import Union , Annotated, Optional
from fastapi import FastAPI , Request , Depends , HTTPException , Query
from pydantic import BaseModel, ConfigDict
from contextlib import asynccontextmanager
from datetime import datetime
import os
from dotenv import load_dotenv

from sqlmodel import SQLModel, Field, create_engine, Session, select, or_

# Load environment variables
load_dotenv()

# MySQL Database Configuration and Default Values
DB_HOST = os.getenv("DB_HOST" , "localhost")
DB_PORT = int(os.getenv("DB_PORT" , "3306"))
DB_USER = os.getenv("DB_USER" , "root")
DB_PASSWORD = os.getenv("DB_PASSWORD" , "")
DB_NAME = os.getenv("DB_NAME" , "bookstore")

# MySQL Database URL
mysql_url = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(
    mysql_url,
    pool_pre_ping=True,
    pool_recycle=300,
    pool_size=10,
    max_overflow=20
)

# def create_db_and_tables():
#     SQLModel.metadata.create_all(engine)
    
def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

@asynccontextmanager
async def lifespan(app: FastAPI):
    # create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

# 1 - Request model
class BookCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    title: str
    author: str
    published_year: int | None = None
    genre: str | None = None

# 2 - Database model
class Book(SQLModel, table=True):
    __tablename__ = "books"
    
    id: int = Field(default=None, primary_key=True)
    title: str = Field(index=True, max_length=255, nullable=False)
    author: str = Field(index=True, max_length=255, nullable=False)
    published_year: int = Field(index=True, nullable=True)
    genre: str = Field(index=True, max_length=100, nullable=True)
    created_at: datetime = Field(default_factory=datetime.now, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.now, nullable=False)

# 3 - Response model
class BookResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    title: str
    author: str
    published_year: int | None
    genre: str | None
    created_at: datetime
    updated_at: datetime

#Dependency
def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()

@app.post("/books", response_model=BookResponse)
def create_book(book_data: BookCreate, db: Session = Depends(get_db)):
    book = Book(
        title=book_data.title,
        author=book_data.author,
        published_year=book_data.published_year,
        genre=book_data.genre)
    
    db.add(book)
    db.commit()
    db.refresh(book)
    return book

@app.get("/books", response_model=list[BookResponse])
def get_books(db: Session = Depends(get_db)):
    books = db.exec(select(Book)).all()
    return books

@app.get("/books/search", response_model=list[BookResponse])
def search_books(
    q: str = Query(..., description="Search term to find in title, author, or genre"),
    db: Session = Depends(get_db)
):
    query = select(Book).where(
        or_(
            Book.title.ilike(f"%{q}%"),
            Book.author.ilike(f"%{q}%"),
            Book.genre.ilike(f"%{q}%"),
            Book.published_year.ilike(f"%{q}%")
        )
    )
    
    books = db.exec(query).all()
    return books

@app.put("/books/{book_id}", response_model=BookResponse)
def update_book(book_id: int, book_data: BookCreate, db: Session = Depends(get_db)):
    book = db.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    book.title = book_data.title
    book.author = book_data.author
    book.published_year = book_data.published_year
    book.genre = book_data.genre
    db.commit()
    db.refresh(book)
    return book

@app.delete("/books/{book_id}", response_model=BookResponse)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(book)
    db.commit()
    return book

@app.get("/books/{book_id}", response_model=BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.get("/")
def health_check():
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
            "version": "1.0.0"
        },
        "database": {
            "type": "MySQL",
            "status": db_status,
            "message": db_message,
            "host": DB_HOST,
            "port": DB_PORT,
            "database": DB_NAME
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




