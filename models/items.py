import datetime
from typing import Optional
from pydantic import BaseModel


class Item(BaseModel):
    id: Optional[int]
    user_id: int
    name: str
    price: int
    description: str
    quantity: int
    is_in_stock: bool = True
    created_at: datetime.datetime
    updated_at: datetime.datetime


class ItemCreate(BaseModel):
    name: str
    price: int
    description: str
    quantity: int


class ItemUpdate(BaseModel):
    name: str
    price: int
    description: str
    quantity: int
