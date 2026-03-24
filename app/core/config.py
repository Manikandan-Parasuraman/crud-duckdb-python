from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Optional
import os

class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI DuckDB CRUD"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # DuckDB Configuration
    DUCKDB_DATABASE: str = "data/duckdb.db"
    
    # CORS Configuration
    BACKEND_CORS_ORIGINS: List[str] = ["*"]
    
    # Logging
    LOG_LEVEL: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True
    )

settings = Settings()

# Ensure data directory exists
os.makedirs(os.path.dirname(settings.DUCKDB_DATABASE), exist_ok=True)
