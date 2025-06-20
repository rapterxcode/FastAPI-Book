from sqlmodel import Session, select, or_
from typing import List, Optional
from models import Book
from schemas import BookCreate, BookUpdate

class BookCRUD:
    @staticmethod
    def create_book(db: Session, book_data: BookCreate) -> Book:
        book = Book(**book_data.model_dump())
        db.add(book)
        db.commit()
        db.refresh(book)
        return book

    @staticmethod
    def get_books(db: Session, skip: int = 0, limit: int = 100) -> List[Book]:
        return db.exec(select(Book).offset(skip).limit(limit)).all()

    @staticmethod
    def get_book(db: Session, book_id: int) -> Optional[Book]:
        return db.get(Book, book_id)

    @staticmethod
    def update_book(db: Session, book_id: int, book_data: BookUpdate) -> Optional[Book]:
        book = db.get(Book, book_id)
        if not book:
            return None
        update_data = book_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(book, field, value)
        db.commit()
        db.refresh(book)
        return book

    @staticmethod
    def delete_book(db: Session, book_id: int) -> Optional[Book]:
        book = db.get(Book, book_id)
        if not book:
            return None
        db.delete(book)
        db.commit()
        return book

    @staticmethod
    def search_books(db: Session, search_term: str) -> List[Book]:
        query = select(Book).where(
            or_(
                Book.title.ilike(f"%{search_term}%"),
                Book.author.ilike(f"%{search_term}%"),
                Book.genre.ilike(f"%{search_term}%"),
                Book.published_year.ilike(f"%{search_term}%")
            )
        )
        return db.exec(query).all()

book_crud = BookCRUD() 