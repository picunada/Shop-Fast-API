from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from models.users import User, UserCreate, UserUpdate, UserResponse
from repositories.users import UserRepository
from .depends import get_user_repository, get_current_user

router = APIRouter()


@router.get("/", response_model=List[UserResponse])
async def read_users(
        users: UserRepository = Depends(get_user_repository),
        limit: int = 100,
        skip: int = 0):
    return await users.get_all(limit=limit, skip=0)


@router.post("/", response_model=UserResponse)
async def create(
        user: UserCreate,
        users: UserRepository = Depends(get_user_repository)):
    return await users.create(u=user)


@router.put("/", response_model=UserResponse)
async def update_user(id: int, user: UserUpdate,
                      users: UserRepository = Depends(get_user_repository),
                      current_user: User = Depends(get_current_user)):
    user = await users.get_by_id(id=id)
    if user is None or user.email != current_user.email:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return await users.update(id=id, u=user)