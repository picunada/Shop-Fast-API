import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, validator, constr

from models.token import Token


class User(BaseModel):
    id: Optional[int] = None
    name: str
    email: EmailStr
    hashed_password: Optional[str]
    is_company: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: constr(min_length=8)
    password2: constr(min_length=8)
    is_company: bool = False

    @validator("password2")
    def password_match(cls, v, values, **kwargs):
        if 'password' in values and v != values["password"]:
            raise ValueError("Password don`t match")
        return v


class UserUpdate(BaseModel):
    name: str
    email: EmailStr
    password: Optional[constr(min_length=8)] = None
    is_company: bool = False


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    is_company: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime


class UserCreateResponse(BaseModel):
    user: Optional[UserResponse]
    token: Optional[Token]
