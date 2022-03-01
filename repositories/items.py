import datetime
from typing import List, Optional

from fastapi import Depends

from db.item import items
from models.items import Item, ItemCreate, ItemUpdate
from models.users import User
from routes.depends import get_current_user
from .base import BaseRepository


class ItemsRepository(BaseRepository):
    async def get_all(self, limit: int = 25, skip: int = 0) -> List[Item]:
        query = items.select().limit(limit).offset(skip)
        return await self.database.fetch_all(query=query)

    async def get_by_id(self, id: int) -> Optional[Item]:
        query = items.select().where(items.c.id == id)
        item = await self.database.fetch_one(query=query)
        if item is None:
            return None
        return Item.parse_obj(item)

    async def create(self, i: ItemCreate, user_id: int, is_in_stock: bool) -> Item:
        item = Item(
            user_id=user_id,
            name=i.name,
            price=i.price,
            description=i.description,
            is_in_stock=is_in_stock,
            created_at=datetime.datetime.utcnow(),
            updated_at=datetime.datetime.utcnow()
        )

        values = {**item.dict()}
        values.pop("id", None)
        query = items.insert().values(**values)
        item.id = await self.database.execute(query=query)
        return item

    async def update(self, id: int, user_id: int, i: ItemUpdate, is_in_stock: bool):
        item = Item(
            user_id=user_id,
            name=i.name,
            price=i.price,
            description=i.description,
            is_in_stock=is_in_stock,
            created_at=datetime.datetime.utcnow(),
            updated_at=datetime.datetime.utcnow()
        )
        values = {**item.dict()}
        values.pop("created_at", None)
        values.pop("id", None)
        query = items.update().where(items.c.id == id).values(**values)
        await self.database.execute(query=query)
        return item

    async def delete(self, id: int):
        query = items.delete().where(items.c.id == id)
        return await self.database.execute(query=query)

