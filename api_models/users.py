from http import HTTPStatus
from typing import Optional

from fastapi import HTTPException
from pydantic import BaseModel, EmailStr, field_validator

from common_api_model import TunedModel
from hashing import Hasher

__all__ = (
    "UserToCreate",
    "UserToUpdate",
    "UserToUpdateProfile",
    "UserToShow",
    "Token",
    "UserPassword"
)


class UserToCreate(BaseModel):
    first_name: str
    last_name: str
    username: EmailStr
    phone: str
    is_staff: Optional[bool] = False
    is_admin: Optional[bool] = False
    is_active: Optional[bool] = True
    password: str

    @field_validator("password")
    def validate_password(cls, value):
        password_exception = HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Придумайте другой пароль"
        )
        if len(value) < 6:
            raise password_exception
        if not any(char.isdigit() for char in value):
            raise password_exception
        if not any(char.isalpha() for char in value):
            raise password_exception
        return Hasher.get_password_hash(value)


class UserToUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[EmailStr] = None
    phone: Optional[str] = None
    is_staff: Optional[bool] = None
    is_admin: Optional[bool] = None
    is_active: Optional[bool] = None


class UserToUpdateProfile(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None


class UserToShow(TunedModel):
    id: int
    first_name: str
    last_name: str
    username: EmailStr
    phone: str
    is_staff: bool
    is_admin: bool


class UserPassword(BaseModel):
    password: str


class Token(BaseModel):
    access_token: str | None = None
    refresh_token: str | None = None
