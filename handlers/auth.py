import token
from datetime import timedelta, datetime, timezone
from http import HTTPStatus
from typing import Annotated, Union

from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic_core._pydantic_core import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from dals.refresh_tokens import RefreshTokenDAL
from database_interaction import get_db
from db_models import User
from global_constants import UserRole
from handlers import get_user_by_username_for_login
from settings import SECRET_KEY, ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/users/token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def authenticate_user(username: str, password: str, session: AsyncSession):
    user = await get_user_by_username_for_login(username, session)
    if not user:
        return False
    if not pwd_context.verify(password, user.password):
        return False
    return user


def create_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=120)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        session: AsyncSession = Depends(get_db),
):
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await get_user_by_username_for_login(username, session)
    if user is None:
        raise credentials_exception
    return user, session


async def check_token_exists(token: str, session: AsyncSession) -> bool:
    token_dal = RefreshTokenDAL(session)
    return await token_dal.check_token_exists(token)


async def create_refresh_token(token: str, session: AsyncSession):
    token_dal = RefreshTokenDAL(session)
    await token_dal.create_refresh_token(token)


async def update_refresh_token(token: str, new_token: str, session: AsyncSession):
    token_dal = RefreshTokenDAL(session)
    await token_dal.update_refresh_token(token, new_token)


class RoleChecker:
    def __init__(self, allowed_roles: list):
        self.allowed_roles = allowed_roles

    def __call__(
            self,
            user_data: Annotated[tuple[User, AsyncSession], Depends(get_current_user)]
    ) -> Union[AsyncSession | None]:
        user, session = user_data
        for role in self.allowed_roles:
            if role == UserRole.STAFF and user.is_staff:
                return session
            elif role == UserRole.ADMIN and user.is_admin:
                return session
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="You don't have enough permissions")


async def validate_refresh_token(
        token: Annotated[str, Depends(oauth2_scheme)],
        session: AsyncSession = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail="Could not validate credentials"
    )
    try:

        if await check_token_exists(token, session):
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            role: str = payload.get("role")
            if username is None or role is None:
                raise credentials_exception
        else:
            raise credentials_exception

    except (JWTError, ValidationError):
        raise credentials_exception

    user = await get_user_by_username_for_login(username, session)

    if user is None:
        raise credentials_exception

    return user, token, session
