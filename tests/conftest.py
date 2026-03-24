import os
import pytest
from typing import Generator
from fastapi.testclient import TestClient
from app.main import app
from app.db.session import get_db, init_db
import duckdb

# Use a separate test database
TEST_DB = "test_data/test.db"

@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    os.makedirs(os.path.dirname(TEST_DB), exist_ok=True)
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)
    # Patch settings to use test db
    from app.core.config import settings
    settings.DUCKDB_DATABASE = TEST_DB
    
    # Initialize DB schema
    init_db()
    yield
    # Cleanup after session
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)

@pytest.fixture
def db_conn() -> Generator[duckdb.DuckDBPyConnection, None, None]:
    conn = duckdb.connect(database=TEST_DB)
    yield conn
    conn.close()

@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as c:
        yield c
