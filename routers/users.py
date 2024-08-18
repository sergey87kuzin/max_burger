from datetime import timedelta
from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from api_models import UserToCreate, UserToShow, Token, UserPassword
from database_interaction import get_db
from db_models import User
from global_constants import UserRole
from handlers import create_new_user
from handlers.auth import authenticate_user, create_token, create_refresh_token, validate_refresh_token, \
    update_refresh_token, RoleChecker, oauth2_scheme, get_current_user
from handlers.users import change_user_password
from hashing import Hasher
from settings import ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_MINUTES

user_router = APIRouter()


@user_router.post("/", response_model=UserToShow)
async def create_user(
        user: UserToCreate,
        session: AsyncSession = Depends(RoleChecker(allowed_roles=["admin"]))
) -> UserToShow:
    created_user = await create_new_user(user, session)
    return created_user


@user_router.post("/change_password/{username}/")
async def change_password(
        username: str,
        new_password: UserPassword,
        user_data: Annotated[tuple[User, AsyncSession], Depends(get_current_user)]
):
    user, session = user_data
    if not user.is_admin and user.username.lower() != username.lower():
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail="Username is incorrect",
        )
    await change_user_password(username=username, password=new_password.password, session=session)


@user_router.post("/token")
async def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        session: AsyncSession = Depends(get_db)
) -> Token:
    user = await authenticate_user(form_data.username, form_data.password, session)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    if user.is_admin:
        role = UserRole.ADMIN
    elif user.is_staff:
        role = UserRole.STAFF
    else:
        role = ""
    access_token = create_token(
        data={"sub": user.username, "role": role},
        expires_delta=access_token_expires
    )
    refresh_token = create_token(
        data={"sub": user.username, "role": role},
        expires_delta=refresh_token_expires
    )
    await create_refresh_token(refresh_token, session)
    return Token(access_token=access_token, refresh_token=refresh_token)


@user_router.post("/refresh")
async def refresh_access_token(
        token_data: Annotated[tuple[User, str, AsyncSession], Depends(validate_refresh_token)],
):
    user, token, session = token_data
    if user.is_admin:
        role = UserRole.ADMIN
    elif user.is_staff:
        role = UserRole.STAFF
    else:
        role = ""
    access_token = create_token(
        data={"sub": user.username, "role": role},
        expires_delta=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    refresh_token = create_token(
        data={"sub": user.username, "role": role},
        expires_delta=REFRESH_TOKEN_EXPIRE_MINUTES
    )
    await update_refresh_token(token, refresh_token, session)
    return Token(access_token=access_token, refresh_token=refresh_token)
