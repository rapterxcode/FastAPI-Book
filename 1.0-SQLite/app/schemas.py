from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class BookCreate(BaseModel):
    """Schema for creating a book"""
    model_config = ConfigDict(from_attributes=True)
    
    title: str
    author: str
    published_year: Optional[int] = None
    genre: Optional[str] = None

class BookResponse(BaseModel):
    """Schema for book response"""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    title: str
    author: str
    published_year: Optional[int]
    genre: Optional[str]
    created_at: datetime
    updated_at: datetime

class BookUpdate(BaseModel):
    """Schema for updating a book"""
    model_config = ConfigDict(from_attributes=True)
    
    title: Optional[str] = None
    author: Optional[str] = None
    published_year: Optional[int] = None
    genre: Optional[str] = None 