"""
Main FastAPI application for BookBloom.
Implements all required API endpoints.
"""

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from datetime import timedelta
from typing import List, Optional, Dict, Any
import os

from .models import (
    Book, BookCreate, User, UserCreate, UserLogin, Token, 
    CartItem, CartResponse
)
from .database import db
from .auth import create_access_token, get_current_user, ACCESS_TOKEN_EXPIRE_MINUTES

app = FastAPI(
    title="BookBloom API",
    description="Books Reborn, Knowledge Renewed - E-commerce API for book catalog",
    version="1.0.0"
)

# CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory cart storage (in production, use Redis or database)
user_carts: Dict[int, List[CartItem]] = {}

# Mount static files
static_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
os.makedirs(static_path, exist_ok=True)
app.mount("/static", StaticFiles(directory=static_path), name="static")

# Serve frontend
@app.get("/")
async def serve_frontend():
    """Serve the main frontend page."""
    frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend", "index.html")
    if os.path.exists(frontend_path):
        return FileResponse(frontend_path)
    return {"message": "BookBloom API - Books Reborn, Knowledge Renewed"}

# Authentication endpoints
@app.post("/api/register", response_model=User)
async def register_user(user: UserCreate):
    """Register a new user."""
    # Check if user already exists
    existing_user = await db.get_user_by_email(user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    try:
        user_data = await db.create_user(
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            password=user.password,
            social_handle_url=user.social_handle_url
        )
        
        return User(
            id=user_data["id"],
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            email=user_data["email"],
            social_handle_url=user_data["social_handle_url"],
            created_at=user_data["created_at"]
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Registration failed"
        )

@app.post("/api/login", response_model=Token)
async def login_user(user_login: UserLogin):
    """Authenticate user and return JWT token."""
    user_data = await db.get_user_by_email(user_login.email)
    
    if not user_data or not db.verify_password(user_login.password, user_data["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user_data["email"]}, 
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/api/me", response_model=User)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current user information."""
    return current_user

# Book catalog endpoints
@app.get("/api/books", response_model=List[Book])
async def get_books(search: Optional[str] = None):
    """Get all books or search by title/author."""
    try:
        books_data = await db.get_books(search)
        return [Book(**book_data) for book_data in books_data]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve books"
        )

@app.get("/api/books/{book_id}", response_model=Book)
async def get_book(book_id: int):
    """Get a specific book by ID."""
    book_data = await db.get_book_by_id(book_id)
    if not book_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    
    return Book(**book_data)

# Cart management endpoints
@app.post("/api/cart/add")
async def add_to_cart(
    cart_item: CartItem, 
    current_user: User = Depends(get_current_user)
):
    """Add book to user's cart."""
    # Verify book exists
    book_data = await db.get_book_by_id(cart_item.book_id)
    if not book_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    
    # Initialize user cart if not exists
    if current_user.id not in user_carts:
        user_carts[current_user.id] = []
    
    # Check if book already in cart
    for item in user_carts[current_user.id]:
        if item.book_id == cart_item.book_id:
            item.quantity += cart_item.quantity
            break
    else:
        user_carts[current_user.id].append(cart_item)
    
    return {"message": "Book added to cart successfully"}

@app.get("/api/cart", response_model=List[CartResponse])
async def get_cart(current_user: User = Depends(get_current_user)):
    """Get user's cart contents."""
    if current_user.id not in user_carts:
        return []
    
    cart_items = []
    for cart_item in user_carts[current_user.id]:
        book_data = await db.get_book_by_id(cart_item.book_id)
        if book_data:
            book = Book(**book_data)
            subtotal = float(book.price or 0) * cart_item.quantity
            cart_items.append(CartResponse(
                book=book,
                quantity=cart_item.quantity,
                subtotal=subtotal
            ))
    
    return cart_items

@app.delete("/api/cart/{book_id}")
async def remove_from_cart(
    book_id: int, 
    current_user: User = Depends(get_current_user)
):
    """Remove book from user's cart."""
    if current_user.id not in user_carts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart is empty"
        )
    
    user_carts[current_user.id] = [
        item for item in user_carts[current_user.id] 
        if item.book_id != book_id
    ]
    
    return {"message": "Book removed from cart"}

@app.put("/api/cart/{book_id}")
async def update_cart_quantity(
    book_id: int, 
    quantity: int,
    current_user: User = Depends(get_current_user)
):
    """Update quantity of book in cart."""
    if current_user.id not in user_carts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart is empty"
        )
    
    if quantity <= 0:
        # Remove item if quantity is 0 or negative
        return await remove_from_cart(book_id, current_user)
    
    for item in user_carts[current_user.id]:
        if item.book_id == book_id:
            item.quantity = quantity
            return {"message": "Cart updated successfully"}
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Book not found in cart"
    )

@app.post("/api/checkout")
async def checkout(current_user: User = Depends(get_current_user)):
    """Process checkout (placeholder implementation)."""
    if current_user.id not in user_carts or not user_carts[current_user.id]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cart is empty"
        )
    
    # Calculate total
    total = 0.0
    cart_items = await get_cart(current_user)
    for item in cart_items:
        total += float(item.subtotal)
    
    # Clear cart (simulate successful order)
    user_carts[current_user.id] = []
    
    return {
        "message": "Order processed successfully",
        "total": total,
        "order_id": f"ORDER_{current_user.id}_{int(os.urandom(4).hex(), 16)}"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)