#!/usr/bin/env python3
"""
Database initialization script for BookBloom application.
Creates SQLite database with books and users tables as per requirements.
"""

import sqlite3
import os
from datetime import datetime

def create_database():
    """Create SQLite database with required tables."""
    
    # Create database directory if it doesn't exist
    db_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
    os.makedirs(db_dir, exist_ok=True)
    
    db_path = os.path.join(db_dir, 'bookbloom.db')
    
    # Connect to database (creates file if doesn't exist)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create books table as per TR-3.3.1
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            isbn TEXT UNIQUE,
            year_of_release INTEGER,
            price DECIMAL,
            category TEXT,
            state TEXT CHECK(state IN ('good', 'fair', 'normal', 'like new'))
        )
    ''')
    
    # Create users table as per TR-3.4.1
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            social_handle_url TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create indexes for better performance
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_books_title ON books(title)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_books_author ON books(author)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)')
    
    conn.commit()
    
    # Insert sample books data
    sample_books = [
        ('The Great Gatsby', 'F. Scott Fitzgerald', '9780743273565', 1925, 12.99, 'Fiction', 'good'),
        ('To Kill a Mockingbird', 'Harper Lee', '9780061120084', 1960, 14.99, 'Fiction', 'like new'),
        ('1984', 'George Orwell', '9780451524935', 1949, 13.99, 'Fiction', 'normal'),
        ('Pride and Prejudice', 'Jane Austen', '9780141439518', 1813, 11.99, 'Romance', 'fair'),
        ('The Catcher in the Rye', 'J.D. Salinger', '9780316769174', 1951, 12.50, 'Fiction', 'good'),
        ('Lord of the Flies', 'William Golding', '9780571056866', 1954, 10.99, 'Fiction', 'normal'),
        ('The Hobbit', 'J.R.R. Tolkien', '9780547928227', 1937, 15.99, 'Fantasy', 'like new'),
        ('Harry Potter and the Sorcerer\'s Stone', 'J.K. Rowling', '9780439708180', 1997, 16.99, 'Fantasy', 'good'),
        ('The Da Vinci Code', 'Dan Brown', '9780307474278', 2003, 13.50, 'Mystery', 'fair'),
        ('The Alchemist', 'Paulo Coelho', '9780062315007', 1988, 12.25, 'Fiction', 'normal'),
    ]
    
    cursor.executemany('''
        INSERT OR IGNORE INTO books (title, author, isbn, year_of_release, price, category, state)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', sample_books)
    
    conn.commit()
    conn.close()
    
    print(f"Database created successfully at: {db_path}")
    print(f"Created {len(sample_books)} sample books")
    
    return db_path

if __name__ == "__main__":
    create_database()