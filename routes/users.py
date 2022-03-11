from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from core.security import create_access_token
from models.token import Token
from models.users import User, UserCreate, UserUpdate, UserResponse, UserCreateResponse
from repositories.cart import CartRepository
from repositories.users import UserRepository
from .depends import get_user_repository, get_current_user, get_cart_repository

router = APIRouter()


@router.get("/", response_model=List[UserResponse])
async def read_users(
        users: UserRepository = Depends(get_user_repository),
        limit: int = 100,
        skip: int = 0):
    return await users.get_all(limit=limit, skip=skip)


@router.post("/", response_model=UserCreateResponse)
async def create(
        user: UserCreate,
        users: UserRepository = Depends(get_user_repository),
        cart: CartRepository = Depends(get_cart_repository)):
    existing_user = await users.get_by_email(user.email)
    if existing_user is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists")
    token = Token(
        access_token=create_access_token({"sub": user.email}),
        token_type="Bearer"
    )
    new_user = await users.create(u=user)
    response = {"user": new_user, "token": token}
    await cart.create(new_user.id)
    return response


@router.patch("/", response_model=UserResponse)
async def update_user(id: int, user: UserUpdate,
                      users: UserRepository = Depends(get_user_repository),
                      current_user: User = Depends(get_current_user)):
    requested_user = await users.get_by_id(id=id)
    if requested_user is None or requested_user.email != current_user.email:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return await users.update(id=id, u=user)
