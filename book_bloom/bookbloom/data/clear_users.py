import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(__file__), "bookbloom.db")

def ensure_users_table(cur):
    """Create users table if it does not exist."""
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            firstname TEXT,
            lastname TEXT,
            email TEXT,
            phone_no TEXT
        )
        """
    )

def clear_users():
    print(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    try:
        cur = conn.cursor()
        # Ensure table exists so that we can guarantee the table is empty afterwards
        ensure_users_table(cur)
        conn.commit()

        # Delete all rows (noop if already empty)
        cur.execute("DELETE FROM users;")
        conn.commit()

        # Report remaining count
        cur.execute("SELECT COUNT(*) FROM users;")
        count = cur.fetchone()[0]
        print(f"Users remaining: {count}")
    finally:
        conn.close()

if __name__ == "__main__":
    clear_users()
