import sqlite3
from pathlib import Path

# ================= DATABASE FILE =================
DB_PATH = Path("receipts.db")


# ================= GET DB CONNECTION =================
def get_db():
    """
    Returns a SQLite connection with row_factory enabled
    so rows behave like dictionaries.
    """
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


# ================= INITIALIZE DATABASE =================
def init_db():
    """
    Creates receipts table if it does not exist.
    Call this once at app startup.
    """
    db = get_db()

    db.execute(
        """
        CREATE TABLE IF NOT EXISTS receipts (
            bill_id TEXT PRIMARY KEY,
            vendor TEXT NOT NULL,
            date TEXT NOT NULL,
            amount REAL NOT NULL,
            tax REAL NOT NULL
        )
        """
    )

    db.commit()
