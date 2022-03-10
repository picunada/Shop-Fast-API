from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from core.tools import is_in_stock
from models.items import Item, ItemCreate, ItemUpdate
from models.users import User
from repositories.items import ItemsRepository
from routes.depends import get_items_repository, get_current_user

router = APIRouter()


@router.get("/", response_model=List[Item])
async def read_items(items: ItemsRepository = Depends(get_items_repository),
                        limit: int = 25,
                        skip: int = 0):
    return await items.get_all(limit=limit, skip=0)


@router.get("/{id}", response_model=Item)
async def get_item_by_id(id: int,
                         items: ItemsRepository = Depends(get_items_repository)):
    item = await items.get_by_id(id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return item


@router.post("/", response_model=Item)
async def create_item(item: ItemCreate,
                      items: ItemsRepository = Depends(get_items_repository),
                      current_user: User = Depends(get_current_user)):
    return await items.create(item, current_user.id, is_in_stock(item.in_stock))


@router.patch("/{id}", response_model=Item)
async def update_item(id: int,
                      item: ItemUpdate,
                      items: ItemsRepository = Depends(get_items_repository),
                      current_user: User = Depends(get_current_user)):
    requested_item = await items.get_by_id(id)
    if requested_item is None or requested_item.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return await items.update(id, current_user.id, item, is_in_stock(item.in_stock))
