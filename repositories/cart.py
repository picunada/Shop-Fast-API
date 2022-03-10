import datetime
from typing import List, Optional

from db.cart import cart
from models.cart import Cart
from .base import BaseRepository


class CartRepository(BaseRepository):
    async def get_all(self, limit: int = 25, skip: int = 0) -> List[Cart]:
        query = cart.select().limit(limit).offset(skip)
        return await self.database.fetch_all(query=query)

    async def get_by_user_id(self, user_id: int) -> Optional[Cart]:
        query = cart.select().where(cart.c.user_id == user_id)
        cart_with_items = await self.database.fetch_one(query=query)
        if cart_with_items is None:
            return None
        return Cart.parse_obj(cart_with_items)

    async def create(self, user_id: int) -> Cart:
        cart_with_items = Cart(
            user_id=user_id,
            items=[],
            updated_at=datetime.datetime.utcnow()
        )
        values = {**cart_with_items.dict()}
        values.pop("id", None)
        query = cart.insert().values(**values)
        cart_with_items.id = await self.database.execute(query=query)
        return cart_with_items

    async def update(self, id: int, user_id: int, c: Cart) -> Cart:
        cart_with_items = Cart(
            id=id,
            user_id=user_id,
            items=c.items,
            updated_at=datetime.datetime.utcnow()
        )
        values = {**cart_with_items.dict()}
        values.pop("id", None)
        query = cart.update().where(cart.c.id == id).values(**values)
        await self.database.execute(query=query)
        return cart_with_items
