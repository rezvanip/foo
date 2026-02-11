#!/usr/bin/env python3
import sqlite3
import os
from typing import Optional


def init_database(db_path: str = "app.db", sql_path: Optional[str] = None):
    """Initialize database with schema."""
    if sql_path is None:
        sql_path = os.path.join(os.path.dirname(__file__), "init.sql")
    
    # Remove existing database for fresh start
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"Removed existing database: {db_path}")
    
    # Create new database
    conn = sqlite3.connect(db_path)
    
    # Read and execute schema
    with open(sql_path, 'r') as f:
        schema = f.read()
    
    conn.executescript(schema)
    conn.commit()
    conn.close()
    
    print(f"Database initialized: {db_path}")


if __name__ == "__main__":
    init_database()
