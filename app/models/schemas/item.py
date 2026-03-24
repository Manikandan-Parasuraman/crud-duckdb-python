from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict
import uuid

# Base Model for properties shared across Create/Update/Read
class ItemBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    price: float = Field(default=0.0, ge=0.0)

# Properties to involve for creating an item
class ItemCreate(ItemBase):
    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()))

# Properties for updating an item (all optional)
class ItemUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    price: Optional[float] = Field(None, ge=0.0)

# Final Schema for the API Response
class Item(ItemBase):
    id: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class ItemListResponse(BaseModel):
    items: List[Item]
    total: int
    offset: int
    limit: int
