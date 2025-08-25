#!/usr/bin/env python3
"""
BookBloom Application Runner
Initializes database and starts the FastAPI server.
"""

import asyncio
import sys
from pathlib import Path

# Add bookbloom package to Python path
project_root = Path(__file__).parent
bookbloom_path = project_root / "bookbloom"
sys.path.insert(0, str(bookbloom_path))

# pylint: disable=import-error,wrong-import-position
from scripts.init_db import create_database


async def main():
    """Initialize database and start the server."""
    print("🌸 Starting BookBloom - Books Reborn, Knowledge Renewed")
    print("=" * 50)

    # Initialize database
    print("Initializing database...")
    try:
        create_database()
        print("✅ Database initialized successfully")
    except Exception as exc:  # pylint: disable=broad-except
        print(f"❌ Database initialization failed: {exc}")
        return 1

    # Start the server
    print("\n🚀 Starting FastAPI server...")
    print("Server will be available at: http://127.0.0.1:8000")
    print("API documentation: http://127.0.0.1:8000/docs")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 50)

    try:
        # pylint: disable=import-outside-toplevel
        import uvicorn

        uvicorn.run(
            "backend.main:app",
            host="127.0.0.1",
            port=8000,
            reload=True,
            access_log=True
        )
    except KeyboardInterrupt:
        print("\n👋 BookBloom server stopped")
        return 0
    except Exception as exc:  # pylint: disable=broad-except
        print(f"❌ Server failed to start: {exc}")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
