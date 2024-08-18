from typing import Optional

from pydantic import BaseModel, EmailStr

from common_api_model import TunedModel


class UserToCreate(BaseModel):
    first_name: str
    last_name: str
    username: EmailStr
    phone: str
    is_staff: Optional[bool] = False
    is_admin: Optional[bool] = False
    is_active: Optional[bool] = True
    password: str


class UserToShow(TunedModel):
    id: int
    first_name: str
    last_name: str
    username: EmailStr
    phone: str
    is_staff: bool
    is_admin: bool
    password: str


class UserToLogin(TunedModel):
    password: str


class Token(BaseModel):
    access_token: str | None = None
    refresh_token: str | None = None
