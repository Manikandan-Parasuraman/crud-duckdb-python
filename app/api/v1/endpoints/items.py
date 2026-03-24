from typing import Any, List
from fastapi import APIRouter, Depends, Query, status
from app.api.deps import get_current_item_service
from app.models.schemas.item import Item, ItemCreate, ItemUpdate, ItemListResponse
from app.services.item_service import ItemService

router = APIRouter()

@router.post("/", response_model=Item, status_code=status.HTTP_201_CREATED)
def create_item(
    item_in: ItemCreate,
    service: ItemService = Depends(get_current_item_service)
) -> Any:
    return service.create_item(item_in)

@router.get("/", response_model=ItemListResponse)
def read_items(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    service: ItemService = Depends(get_current_item_service)
) -> Any:
    return service.get_items(skip=skip, limit=limit)

@router.get("/{item_id}", response_model=Item)
def read_item(
    item_id: str,
    service: ItemService = Depends(get_current_item_service)
) -> Any:
    return service.get_item(item_id)

@router.put("/{item_id}", response_model=Item)
def update_item(
    item_id: str,
    item_in: ItemUpdate,
    service: ItemService = Depends(get_current_item_service)
) -> Any:
    return service.update_item(item_id, item_in)

@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(
    item_id: str,
    service: ItemService = Depends(get_current_item_service)
) -> None:
    service.delete_item(item_id)
    return None
