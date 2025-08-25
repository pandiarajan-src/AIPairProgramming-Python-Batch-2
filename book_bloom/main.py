from pathlib import Path
from datetime import datetime
from typing import List, Generator

from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from passlib.hash import bcrypt
from pydantic import BaseModel
from sqlalchemy import (
    Column,
    DateTime,
    Float,
    Integer,
    String,
    CheckConstraint,
    create_engine,
)
from sqlalchemy.orm import Session, declarative_base, sessionmaker

BASE_DIR = Path(__file__).resolve().parent
DATABASE_URL = f"sqlite:///{BASE_DIR / 'bookbloom.db'}"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    isbn = Column(String, unique=True)
    year_of_release = Column(Integer)
    price = Column(Float)
    category = Column(String)
    state = Column(
        String,
        CheckConstraint("state in ('good','fair','normal','like new')"),
    )


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    social_handle_url = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)


def init_db() -> None:
    """Create tables and insert dummy data if necessary."""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        if db.query(Book).count() == 0:
            books = [
                Book(
                    title="The Hobbit",
                    author="J.R.R. Tolkien",
                    isbn="978-0-123456-47-2",
                    year_of_release=1937,
                    price=10.99,
                    category="Fantasy",
                    state="good",
                ),
                Book(
                    title="1984",
                    author="George Orwell",
                    isbn="978-0-987654-32-1",
                    year_of_release=1949,
                    price=8.99,
                    category="Dystopian",
                    state="like new",
                ),
            ]
            db.add_all(books)
        if db.query(User).count() == 0:
            user = User(
                first_name="John",
                last_name="Doe",
                email="john@example.com",
                password_hash=bcrypt.hash("password"),
                social_handle_url="https://twitter.com/john",
            )
            db.add(user)
        db.commit()
    finally:
        db.close()


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class BookSchema(BaseModel):
    id: int
    title: str
    author: str
    isbn: str | None = None
    year_of_release: int | None = None
    price: float | None = None
    category: str | None = None
    state: str | None = None

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str
    social_handle_url: str | None = None


class UserLogin(BaseModel):
    email: str
    password: str


app = FastAPI(title="BookBloom", description="Books Reborn, Knowledge Renewed")


@app.on_event("startup")
def on_startup() -> None:
    init_db()


@app.get("/api/books", response_model=List[BookSchema])
def list_books(db: Session = Depends(get_db)) -> List[Book]:
    return db.query(Book).all()


@app.get("/api/books/search", response_model=List[BookSchema])
def search_books(q: str, db: Session = Depends(get_db)) -> List[Book]:
    query = f"%{q}%"
    return (
        db.query(Book)
        .filter((Book.title.ilike(query)) | (Book.author.ilike(query)))
        .all()
    )


@app.post("/api/users", status_code=201)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    db_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        password_hash=bcrypt.hash(user.password),
        social_handle_url=user.social_handle_url,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"id": db_user.id, "email": db_user.email}


@app.post("/api/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not bcrypt.verify(user.password, db_user.password_hash):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    return {"message": "Login successful"}


app.mount(
    "/",
    StaticFiles(directory=BASE_DIR / "frontend", html=True),
    name="static",
)
