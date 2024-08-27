from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api_models import UserToCreate, UserToShow, UserToUpdate, UserToUpdateProfile

__all__ = (
    "create_new_user",
    "get_user_by_username_for_login",
    "change_user_password",
    "_update_user",
)

from dals import UserDAL
from db_models import User


async def create_new_user(body: UserToCreate, session: AsyncSession) -> UserToShow:
    async with session.begin():
        user_dal = UserDAL(session)
        if await user_dal.get_user_by_username(username=body.username):
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=f"User with username {body.username} already exists"
            )
        user = await user_dal.create_user(body)
        return UserToShow.model_validate(user, from_attributes=True)


async def get_user_by_username_for_login(username: str, session: AsyncSession) -> User:
    async with session.begin():
        user_dal = UserDAL(session)
        return await user_dal.get_user_by_username(username)


async def change_user_password(username: str, password: str, session: AsyncSession) -> None:
    async with session.begin():
        user_dal = UserDAL(session)
        return await user_dal.change_user_password(username, password)


async def _update_user(user_id: int, body: UserToUpdateProfile, session: AsyncSession) -> UserToShow:
    async with session.begin():
        user_dal = UserDAL(session)
        user = await user_dal.update_user(user_id, body)
        return UserToShow.model_validate(user)
