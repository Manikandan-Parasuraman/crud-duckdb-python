import duckdb
from typing import Generator, Any
from contextlib import contextmanager
from app.core.config import settings
import threading

# Use a thread-local for duckdb connections to avoid conflicts if needed,
# though DuckDB's native connection is thread-safe for reading.
# For production, we'll keep a primary shared connection.

_db_conn = None
_lock = threading.Lock()

def get_db_connection() -> duckdb.DuckDBPyConnection:
    global _db_conn
    if _db_conn is None:
        with _lock:
            if _db_conn is None:
                _db_conn = duckdb.connect(database=settings.DUCKDB_DATABASE)
                # Enable concurrent access and thread safety
                _db_conn.execute("PRAGMA threads=4;") 
    return _db_conn

def init_db() -> None:
    """Initialize tables if they don't exist"""
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id VARCHAR PRIMARY KEY,
            title VARCHAR NOT NULL,
            description VARCHAR,
            price DOUBLE DEFAULT 0.0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

def get_db() -> Generator[duckdb.DuckDBPyConnection, None, None]:
    """Dependency for FastAPI"""
    conn = get_db_connection()
    try:
        yield conn
    finally:
        # We don't close the shared connection as it's managed globally
        pass
