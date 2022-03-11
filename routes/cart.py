from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from models.cart import CartResponse
from models.items import ItemInCart
from models.users import User
from repositories.cart import CartRepository
from repositories.items import ItemsRepository
from routes.depends import get_cart_repository, get_current_user, get_items_repository

router = APIRouter()


@router.get("/", response_model=List[CartResponse])
async def read_carts(cart: CartRepository = Depends(get_cart_repository),
                     limit: int = 25,
                     skip: int = 0):
    carts = await cart.get_all(limit=limit, skip=skip)
    return carts


@router.get("/me", response_model=CartResponse)
async def get_cart(cart_repo: CartRepository = Depends(get_cart_repository),
                   current_user: User = Depends(get_current_user)):
    cart = await cart_repo.get_by_user_id(current_user.id)
    if cart is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart not found")
    return cart


@router.patch("/add", response_model=CartResponse)
async def add_item(item_id: int,
                   quantity: int,
                   cart_repo: CartRepository = Depends(get_cart_repository),
                   items: ItemsRepository = Depends(get_items_repository),
                   current_user: User = Depends(get_current_user)):
    item = await items.get_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    cart = await cart_repo.get_by_user_id(current_user.id)
    cart_id_list = list()
    for i in cart.items:
        cart_id_list.append(i.item.id)
    if item.id not in cart_id_list:
        new_item = ItemInCart(
            item=item,
            quantity=quantity
        )
        cart.items.append(new_item)
    else:
        for i in cart.items:
            if i.item.id == item.id:
                i.quantity += quantity

    new_cart = await cart_repo.update(cart.id, current_user.id, cart)
    return new_cart


@router.patch("/delete", response_model=CartResponse)
async def delete_item(item_id: int,
                      quantity: int,
                      cart_repo: CartRepository = Depends(get_cart_repository),
                      items: ItemsRepository = Depends(get_items_repository),
                      current_user: User = Depends(get_current_user)):
    item = await items.get_by_id(item_id)
    cart = await cart_repo.get_by_user_id(current_user.id)
    cart_id_list = list()
    for i in cart.items:
        cart_id_list.append(i.item.id)
    if item.id not in cart_id_list:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    else:
        for i in cart.items:
            if item.id == i.item.id and quantity == i.quantity:
                cart.items.remove(i)
            elif item.id == i.item.id and quantity < i.quantity:
                i.quantity -= quantity
            else:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                    detail="Requested quantity is more than expected")

    new_cart = await cart_repo.update(cart.id, current_user.id, cart)
    return new_cart
