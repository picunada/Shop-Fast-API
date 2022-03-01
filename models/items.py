import datetime
from typing import Optional
from pydantic import BaseModel


class Item(BaseModel):
    id: Optional[int]
    user_id: int
    name: str
    price: int
    description: str
    is_in_stock: bool = True
    created_at: datetime.datetime
    updated_at: datetime.datetime


class ItemCreate(BaseModel):
    name: str(max_length=20)
    price: int
    description: str(max_length=256)
    items_in_stock: int


class ItemUpdate(BaseModel):
    name: str(max_length=20)
    price: int
    description: str(max_length=256)
    items_in_stock: int
