from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class Book(SQLModel, table=True):
    """Book database model"""
    __tablename__ = "books"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True, max_length=255, nullable=False)
    author: str = Field(index=True, max_length=255, nullable=False)
    published_year: Optional[int] = Field(index=True, nullable=True)
    genre: Optional[str] = Field(index=True, max_length=100, nullable=True)
    created_at: datetime = Field(default_factory=datetime.now, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.now, nullable=False) 