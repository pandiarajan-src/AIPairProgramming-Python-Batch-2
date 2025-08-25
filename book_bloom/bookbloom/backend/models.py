"""
Pydantic models for BookBloom application.
Defines data models for API requests and responses.
"""

from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from decimal import Decimal

class BookBase(BaseModel):
    title: str
    author: str
    isbn: Optional[str] = None
    year_of_release: Optional[int] = None
    price: Optional[Decimal] = None
    category: Optional[str] = None
    state: Optional[str] = None

class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: int
    
    class Config:
        from_attributes = True

class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    social_handle_url: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class User(UserBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class UserInDB(User):
    password_hash: str

class Token(BaseModel):
    access_token: str
    token_type: str

class CartItem(BaseModel):
    book_id: int
    quantity: int = 1

class CartResponse(BaseModel):
    book: Book
    quantity: int
    subtotal: Decimal