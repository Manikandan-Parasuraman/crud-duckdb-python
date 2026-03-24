from fastapi import Depends
import duckdb
from app.db.session import get_db
from app.repositories.item_repository import ItemRepository, get_item_repository
from app.services.item_service import ItemService, get_item_service

def get_current_item_repository(
    db: duckdb.DuckDBPyConnection = Depends(get_db)
) -> ItemRepository:
    return get_item_repository(db)

def get_current_item_service(
    repository: ItemRepository = Depends(get_current_item_repository)
) -> ItemService:
    return get_item_service(repository)
