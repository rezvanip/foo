"""Database connection management using SQLite singleton pattern."""
import sqlite3
from contextlib import contextmanager
from typing import Optional


class DatabaseConnection:
    """Singleton managing a single SQLite connection instance."""
    
    _instance: Optional['DatabaseConnection'] = None
    _db_path: str = "app.db"
    
    def __new__(cls):
        """Ensure only one connection instance exists."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize connection holder."""
        self._connection: Optional[sqlite3.Connection] = None
    
    @classmethod
    def set_db_path(cls, path: str):
        """Set database file path."""
        cls._db_path = path
    
    def get_connection(self) -> sqlite3.Connection:
        """Get or create SQLite connection with row factory."""
        if self._connection is None:
            self._connection = sqlite3.connect(self._db_path)
            self._connection.row_factory = sqlite3.Row
        return self._connection
    
    def close(self):
        """Close database connection."""
        if self._connection:
            self._connection.close()
            self._connection = None


@contextmanager
def get_db():
    """Context manager handling transactions with automatic commit/rollback."""
    db = DatabaseConnection()
    conn = db.get_connection()
    try:
        yield conn
    except Exception:
        conn.rollback()
        raise
    else:
        conn.commit()
