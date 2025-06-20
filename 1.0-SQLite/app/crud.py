from sqlmodel import Session, select, or_
from typing import List, Optional
from .models import Book
from .schemas import BookCreate, BookUpdate

class BookCRUD:
    """CRUD operations for Book model"""
    
    @staticmethod
    def create_book(db: Session, book_data: BookCreate) -> Book:
        """Create a new book"""
        book = Book(
            title=book_data.title,
            author=book_data.author,
            published_year=book_data.published_year,
            genre=book_data.genre
        )
        db.add(book)
        db.commit()
        db.refresh(book)
        return book
    
    @staticmethod
    def get_books(db: Session, skip: int = 0, limit: int = 100) -> List[Book]:
        """Get all books with pagination"""
        books = db.exec(select(Book).offset(skip).limit(limit)).all()
        return books
    
    @staticmethod
    def get_book(db: Session, book_id: int) -> Optional[Book]:
        """Get a book by ID"""
        return db.get(Book, book_id)
    
    @staticmethod
    def update_book(db: Session, book_id: int, book_data: BookUpdate) -> Optional[Book]:
        """Update a book"""
        book = db.get(Book, book_id)
        if not book:
            return None
        
        # Update only provided fields
        update_data = book_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(book, field, value)
        
        db.commit()
        db.refresh(book)
        return book
    
    @staticmethod
    def delete_book(db: Session, book_id: int) -> Optional[Book]:
        """Delete a book"""
        book = db.get(Book, book_id)
        if not book:
            return None
        
        db.delete(book)
        db.commit()
        return book
    
    @staticmethod
    def search_books(db: Session, search_term: str) -> List[Book]:
        """Search books by term"""
        query = select(Book).where(
            or_(
                Book.title.ilike(f"%{search_term}%"),
                Book.author.ilike(f"%{search_term}%"),
                Book.genre.ilike(f"%{search_term}%"),
                Book.published_year.ilike(f"%{search_term}%")
            )
        )
        books = db.exec(query).all()
        return books

# Create CRUD instance
book_crud = BookCRUD() 