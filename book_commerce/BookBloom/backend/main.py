from fastapi import FastAPI
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
import sqlite3
import os
import logging

app = FastAPI(title="BookBloom", description="Old books blossoming into new learning")

# Add detailed logging for debugging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("bookbloom")

# Simplify the frontend path resolution
frontend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../frontend"))
logger.debug(f"Starting FastAPI application with frontend path: {frontend_path}")
app.mount("/frontend", StaticFiles(directory=frontend_path), name="frontend")

# Debugging: Check if the frontend directory and index.html exist
if not os.path.exists(frontend_path):
    logger.error(f"Frontend directory does not exist at {frontend_path}")
if not os.path.exists(os.path.join(frontend_path, "index.html")):
    logger.error(f"index.html does not exist in the frontend directory")

def get_db_connection():
    conn = sqlite3.connect("../database/bookbloom.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.get("/books")
def get_books():
    conn = get_db_connection()
    books = conn.execute("SELECT * FROM books").fetchall()
    conn.close()
    return JSONResponse(content={"books": [dict(book) for book in books]})

@app.get("/users")
def get_users():
    conn = get_db_connection()
    users = conn.execute("SELECT * FROM users").fetchall()
    conn.close()
    return JSONResponse(content={"users": [dict(user) for user in users]})

@app.get("/")
def root():
    return RedirectResponse(url="/frontend/index.html", status_code=302)

# Serve a test static file to verify StaticFiles configuration
@app.get("/test")
def test_static():
    return JSONResponse(content={"message": "Static file serving is working"})
