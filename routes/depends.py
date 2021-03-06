from fastapi import Depends, HTTPException, status

from repositories.cart import CartRepository
from repositories.items import ItemsRepository
from repositories.users import UserRepository
from db.connect import database
from core.security import JWTBearer, decode_access_token
from models.users import User


def get_user_repository() -> UserRepository:
    return UserRepository(database)


def get_items_repository() -> ItemsRepository:
    return ItemsRepository(database)


def get_cart_repository() -> CartRepository:
    return CartRepository(database)


async def get_current_user(
        users: UserRepository = Depends(get_user_repository),
        token: str = Depends(JWTBearer()),
) -> User:
    cred_exception = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Credentials are not valid")
    payload = decode_access_token(token)
    if payload is None:
        raise cred_exception

    email: str = payload.get("sub")
    if email is None:
        raise cred_exception

    user = await users.get_by_email(email=email)
    if user is None:
        raise cred_exception
    return user
