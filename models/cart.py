import datetime
from typing import Optional, List, Dict
from pydantic import BaseModel
from .items import Item, ItemUpdate, ItemInCart


class Cart(BaseModel):
    id: Optional[int]
    user_id: int
    items: Optional[List[ItemInCart]]
    updated_at: datetime.datetime

    class Config:
        orm_mode = True


class CartResponse(BaseModel):
    id: Optional[int]
    user_id: int
    items: Optional[List[ItemInCart]]
    updated_at: datetime.datetime

