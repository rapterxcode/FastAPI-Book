from fastapi import APIRouter, HTTPException, Query
from typing import List
from ....crud import book_crud
from ....schemas import BookCreate, BookResponse, BookUpdate
from ....api.deps import SessionDep

router = APIRouter()

@router.post("", response_model=BookResponse)
def create_book(book_data: BookCreate, db: SessionDep):
    """Create a new book"""
    return book_crud.create_book(db, book_data)

@router.get("", response_model=List[BookResponse])
def get_books(
    db: SessionDep,
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return")
):
    """Get all books with pagination"""
    return book_crud.get_books(db, skip=skip, limit=limit)

@router.get("/search", response_model=List[BookResponse])
def search_books(
    db: SessionDep,
    q: str = Query(..., description="Search term to find in title, author, or genre")
):
    """Search books by term"""
    return book_crud.search_books(db, q)

@router.get("/{book_id}", response_model=BookResponse)
def get_book(book_id: int, db: SessionDep):
    """Get a book by ID"""
    book = book_crud.get_book(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.put("/{book_id}", response_model=BookResponse)
def update_book(book_id: int, book_data: BookUpdate, db: SessionDep):
    """Update a book"""
    book = book_crud.update_book(db, book_id, book_data)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.delete("/{book_id}", response_model=BookResponse)
def delete_book(book_id: int, db: SessionDep):
    """Delete a book"""
    book = book_crud.delete_book(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book 