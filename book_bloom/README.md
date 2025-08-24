# BookBloom 🌸
**Books Reborn, Knowledge Renewed**

A modern e-commerce platform for books built with FastAPI backend and vanilla JavaScript frontend.

## Features

- 📚 Book catalog with search functionality
- 👤 User registration and authentication
- 🛒 Shopping cart management
- 💳 Checkout process
- 🔐 JWT-based authentication
- 📱 Responsive web design

## Quick Start

### Prerequisites
- Python 3.12 or higher
- uv (recommended) or pip for package management

### Installation & Running

#### Option 1: Using the startup script (recommended)
```bash
./start.sh
```

#### Option 2: Manual setup
```bash
# Install dependencies
cd bookbloom
uv sync  # or pip install -e .

# Initialize database and start server
cd ..
python run.py
```

### Access the Application
- Frontend: http://127.0.0.1:8000
- API Documentation: http://127.0.0.1:8000/docs
- API: http://127.0.0.1:8000/api/

## Project Structure

```
book_bloom/
├── bookbloom/
│   ├── backend/           # FastAPI backend
│   │   ├── main.py       # Main FastAPI application
│   │   ├── models.py     # Pydantic models
│   │   ├── database.py   # Database operations
│   │   └── auth.py       # Authentication logic
│   ├── frontend/         # Frontend HTML
│   ├── static/           # CSS and JavaScript
│   ├── scripts/          # Database initialization
│   └── pyproject.toml    # Dependencies
├── run.py                # Application runner
├── start.sh              # Startup script
└── README.md
```

## API Endpoints

### Authentication
- `POST /api/register` - Register new user
- `POST /api/login` - User login
- `GET /api/me` - Get current user info

### Books
- `GET /api/books` - Get all books (with optional search)
- `GET /api/books/{id}` - Get specific book

### Cart
- `POST /api/cart/add` - Add book to cart
- `GET /api/cart` - Get cart contents
- `PUT /api/cart/{book_id}` - Update quantity
- `DELETE /api/cart/{book_id}` - Remove from cart
- `POST /api/checkout` - Process checkout

## Development

The application uses:
- **Backend**: FastAPI with SQLite database
- **Frontend**: Vanilla HTML/CSS/JavaScript
- **Authentication**: JWT tokens with bcrypt password hashing
- **Database**: SQLite with aiosqlite for async operations

## Testing

To test the application manually:
1. Start the server: `./start.sh`
2. Open http://127.0.0.1:8000 in your browser
3. Register a new account
4. Browse books and add them to cart
5. Test the checkout process