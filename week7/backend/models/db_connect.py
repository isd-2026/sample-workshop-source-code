import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # Path to the folder that contains db_connect.py
DB_NAME = os.path.join(BASE_DIR, "../../db/", "app.db")  # your SQLite file

def get_connection():
    """Create and return a database connection."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  # return rows as dict-like objects
    return conn