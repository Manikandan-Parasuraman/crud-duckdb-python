import duckdb
import uuid
from datetime import datetime
from typing import List, Optional, Tuple
from app.models.schemas.item import ItemCreate, ItemUpdate, Item
from app.core.exceptions import EntityNotFoundError, RepositoryError

class ItemRepository:
    def __init__(self, db: duckdb.DuckDBPyConnection):
        self.db = db

    def create(self, obj_in: ItemCreate) -> Item:
        item_id = obj_in.id or str(uuid.uuid4())
        created_at = datetime.now()
        updated_at = created_at
        
        try:
            self.db.execute(
                "INSERT INTO items (id, title, description, price, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?)",
                (item_id, obj_in.title, obj_in.description, obj_in.price, created_at, updated_at)
            )
            return self.get_by_id(item_id)
        except Exception as e:
            raise RepositoryError(f"Error creating item: {str(e)}")

    def get_by_id(self, item_id: str) -> Item:
        result = self.db.execute(
            "SELECT id, title, description, price, created_at, updated_at FROM items WHERE id = ?",
            (item_id,)
        ).fetchone()
        
        if not result:
            raise EntityNotFoundError("Item", item_id)
        
        # Mapping DuckDB tuple to Item schema
        return Item(
            id=result[0],
            title=result[1],
            description=result[2],
            price=result[3],
            created_at=result[4],
            updated_at=result[5]
        )

    def get_multi(self, offset: int = 0, limit: int = 10) -> Tuple[List[Item], int]:
        # Get count
        total = self.db.execute("SELECT COUNT(*) FROM items").fetchone()[0]
        # Get results
        results = self.db.execute(
            "SELECT id, title, description, price, created_at, updated_at FROM items LIMIT ? OFFSET ?",
            (limit, offset)
        ).fetchall()
        
        items = [
            Item(
                id=r[0],
                title=r[1],
                description=r[2],
                price=r[3],
                created_at=r[4],
                updated_at=r[5]
            ) for r in results
        ]
        return items, total

    def update(self, item_id: str, obj_in: ItemUpdate) -> Item:
        # Check if exists
        self.get_by_id(item_id)
        
        # Build dynamic update query
        update_data = obj_in.model_dump(exclude_unset=True)
        if not update_data:
             return self.get_by_id(item_id)

        update_data["updated_at"] = datetime.now()
        
        cols = ", ".join([f"{k} = ?" for k in update_data.keys()])
        vals = list(update_data.values())
        vals.append(item_id)

        try:
            self.db.execute(f"UPDATE items SET {cols} WHERE id = ?", vals)
            return self.get_by_id(item_id)
        except Exception as e:
            raise RepositoryError(f"Error updating item: {str(e)}")

    def delete(self, item_id: str) -> bool:
        # Check if exists
        self.get_by_id(item_id)
        try:
            self.db.execute("DELETE FROM items WHERE id = ?", (item_id,))
            return True
        except Exception as e:
            raise RepositoryError(f"Error deleting item: {str(e)}")

def get_item_repository(db: duckdb.DuckDBPyConnection) -> ItemRepository:
    return ItemRepository(db)
