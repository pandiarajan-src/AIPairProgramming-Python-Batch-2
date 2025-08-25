"""
Database connection and operations for BookBloom application.
Handles SQLite database interactions using aiosqlite.
"""

import aiosqlite
import os
from typing import List, Optional, Dict, Any
from decimal import Decimal
from datetime import datetime
from passlib.context import CryptContext
import warnings

# Suppress bcrypt version warnings for compatibility
warnings.filterwarnings("ignore", message=".*bcrypt version.*")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Database:
    def __init__(self, db_path: str = None):
        if db_path is None:
            # Default to data/bookbloom.db relative to project root
            project_root = os.path.dirname(os.path.dirname(__file__))
            self.db_path = os.path.join(project_root, 'data', 'bookbloom.db')
        else:
            self.db_path = db_path
    
    async def get_connection(self):
        """Get database connection."""
        return aiosqlite.connect(self.db_path)
    
    # Book operations
    async def get_books(self, search: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get all books or search by title/author."""
        async with await self.get_connection() as db:
            if search:
                query = """
                    SELECT id, title, author, isbn, year_of_release, price, category, state 
                    FROM books 
                    WHERE LOWER(title) LIKE LOWER(?) OR LOWER(author) LIKE LOWER(?)
                    ORDER BY title
                """
                search_term = f"%{search}%"
                cursor = await db.execute(query, (search_term, search_term))
            else:
                query = """
                    SELECT id, title, author, isbn, year_of_release, price, category, state 
                    FROM books 
                    ORDER BY title
                """
                cursor = await db.execute(query)
            
            rows = await cursor.fetchall()
            columns = [description[0] for description in cursor.description]
            return [dict(zip(columns, row)) for row in rows]
    
    async def get_book_by_id(self, book_id: int) -> Optional[Dict[str, Any]]:
        """Get a single book by ID."""
        async with await self.get_connection() as db:
            query = """
                SELECT id, title, author, isbn, year_of_release, price, category, state 
                FROM books 
                WHERE id = ?
            """
            cursor = await db.execute(query, (book_id,))
            row = await cursor.fetchone()
            
            if row:
                columns = [description[0] for description in cursor.description]
                return dict(zip(columns, row))
            return None
    
    # User operations
    async def create_user(self, first_name: str, last_name: str, email: str, 
                         password: str, social_handle_url: Optional[str] = None) -> Dict[str, Any]:
        """Create a new user."""
        password_hash = pwd_context.hash(password)
        
        async with await self.get_connection() as db:
            query = """
                INSERT INTO users (first_name, last_name, email, password_hash, social_handle_url)
                VALUES (?, ?, ?, ?, ?)
            """
            cursor = await db.execute(query, (first_name, last_name, email, password_hash, social_handle_url))
            await db.commit()
            
            user_id = cursor.lastrowid
            return await self.get_user_by_id(user_id)
    
    async def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Get user by email."""
        async with await self.get_connection() as db:
            query = """
                SELECT id, first_name, last_name, email, password_hash, social_handle_url, created_at
                FROM users 
                WHERE email = ?
            """
            cursor = await db.execute(query, (email,))
            row = await cursor.fetchone()
            
            if row:
                columns = [description[0] for description in cursor.description]
                return dict(zip(columns, row))
            return None
    
    async def get_user_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Get user by ID."""
        async with await self.get_connection() as db:
            query = """
                SELECT id, first_name, last_name, email, password_hash, social_handle_url, created_at
                FROM users 
                WHERE id = ?
            """
            cursor = await db.execute(query, (user_id,))
            row = await cursor.fetchone()
            
            if row:
                columns = [description[0] for description in cursor.description]
                return dict(zip(columns, row))
            return None
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify password against hash."""
        return pwd_context.verify(plain_password, hashed_password)

# Global database instance
db = Database()