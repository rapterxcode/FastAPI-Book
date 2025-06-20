from sqlmodel import Session, select
from typing import List, Optional
from models import Book
from schemas import BookCreate, BookResponse, BookUpdate
from crud import book_crud
from datetime import datetime

class BookService:
    @staticmethod
    def create_book(db: Session, book_data: BookCreate) -> BookResponse:
        book = book_crud.create_book(db, book_data)
        return BookResponse.model_validate(book)

    @staticmethod
    def get_books(db: Session, skip: int = 0, limit: int = 100) -> List[BookResponse]:
        books = book_crud.get_books(db, skip=skip, limit=limit)
        return [BookResponse.model_validate(book) for book in books]

    @staticmethod
    def get_book(db: Session, book_id: int) -> Optional[BookResponse]:
        book = book_crud.get_book(db, book_id)
        if book:
            return BookResponse.model_validate(book)
        return None

    @staticmethod
    def update_book(db: Session, book_id: int, book_data: BookUpdate) -> Optional[BookResponse]:
        book = book_crud.update_book(db, book_id, book_data)
        if book:
            return BookResponse.model_validate(book)
        return None

    @staticmethod
    def delete_book(db: Session, book_id: int) -> Optional[BookResponse]:
        book = book_crud.delete_book(db, book_id)
        if book:
            return BookResponse.model_validate(book)
        return None

    @staticmethod
    def search_books(db: Session, search_term: str) -> List[BookResponse]:
        books = book_crud.search_books(db, search_term)
        return [BookResponse.model_validate(book) for book in books]

book_service = BookService() 