from typing import List

from fastapi import APIRouter, Depends

from models.users import User, UserInput
from repositories.users import UserRepository
from .depends import get_user_repository

router = APIRouter()


@router.get("/", response_model=List[User])
async def read_users(
        users: UserRepository = Depends(get_user_repository),
        limit: int = 100,
        skip: int = 0):
    return await users.get_all(limit=limit, skip=0)


@router.post("/", response_model=User)
async def create(
        user: UserInput,
        users: UserRepository = Depends(get_user_repository)):
    return await users.create(u=user)
