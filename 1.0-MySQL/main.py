from fastapi import FastAPI, HTTPException, Query, Depends
from typing import List
from database import lifespan, get_session, engine
from schemas import BookCreate, BookResponse, BookUpdate
from service import book_service
from config import PORT, APP_NAME, APP_VERSION, APP_DESCRIPTION, DB_HOST, DB_PORT, DB_NAME
from sqlmodel import Session, select
from models import Book
from datetime import datetime


app = FastAPI(lifespan=lifespan)

def health_check():
    try:
        with Session(engine) as session:
            session.exec(select(Book).limit(1))
            db_status = "Connected"
            db_message = "Database connection successful"
    except Exception as e:
        db_status = "Error"
        db_message = f"Database connection failed: {str(e)}"
    return {
        "status": "healthy" if db_status == "Connected" else "unhealthy",
        "server": {
            "Deverlop by": "Phone",
            "status": "Running",
            "timestamp": datetime.now().isoformat(),
            "framework": "FastAPI",
            "name": APP_NAME,
            "version": APP_VERSION,
            "description": APP_DESCRIPTION,
        },
        "database": {
            "type": "MySQL",
            "status": db_status,
            "message": db_message,
            "host": DB_HOST,
            "port": DB_PORT,
            "database": DB_NAME
        }
    }

@app.get("/")
def root():
    return health_check()

@app.post("/books", response_model=BookResponse)
def create_book(book_data: BookCreate, db: Session = Depends(get_session)):
    return book_service.create_book(db, book_data)

@app.get("/books", response_model=List[BookResponse])
def get_books(db: Session = Depends(get_session), skip: int = 0, limit: int = 100):
    return book_service.get_books(db, skip=skip, limit=limit)

@app.get("/books/search", response_model=List[BookResponse])
def search_books(q: str = Query(..., description="Search term to find in title, author, or genre"), db: Session = Depends(get_session)):
    return book_service.search_books(db, q)

@app.get("/books/{book_id}", response_model=BookResponse)
def get_book(book_id: int, db: Session = Depends(get_session)):
    book = book_service.get_book(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.put("/books/{book_id}", response_model=BookResponse)
def update_book(book_id: int, book_data: BookUpdate, db: Session = Depends(get_session)):
    book = book_service.update_book(db, book_id, book_data)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.delete("/books/{book_id}", response_model=BookResponse)
def delete_book(book_id: int, db: Session = Depends(get_session)):
    book = book_service.delete_book(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book




