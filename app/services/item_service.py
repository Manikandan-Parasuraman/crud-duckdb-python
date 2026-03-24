from typing import List, Tuple
from app.models.schemas.item import ItemCreate, ItemUpdate, Item, ItemListResponse
from app.repositories.item_repository import ItemRepository

class ItemService:
    def __init__(self, repository: ItemRepository):
        self.repository = repository

    def create_item(self, item_in: ItemCreate) -> Item:
        return self.repository.create(item_in)

    def get_item(self, item_id: str) -> Item:
        return self.repository.get_by_id(item_id)

    def get_items(self, skip: int = 0, limit: int = 10) -> ItemListResponse:
        items, total = self.repository.get_multi(offset=skip, limit=limit)
        return ItemListResponse(
            items=items,
            total=total,
            offset=skip,
            limit=limit
        )

    def update_item(self, item_id: str, item_in: ItemUpdate) -> Item:
        return self.repository.update(item_id, item_in)

    def delete_item(self, item_id: str) -> bool:
        return self.repository.delete(item_id)

def get_item_service(repository: ItemRepository) -> ItemService:
    return ItemService(repository)
