from sqlalchemy.ext.asyncio import AsyncSession

from api_models import UserToCreate, UserToShow


__all__ = (
    "create_new_user",
    "get_user_by_username_for_login"
)

from dals import UserDAL
from db_models import User


async def create_new_user(body: UserToCreate, session: AsyncSession) -> UserToShow:
    user_dal = UserDAL(session)
    user = await user_dal.create_user(body)
    return UserToShow.model_validate(user, from_attributes=True)


async def get_user_by_username_for_login(username: str, session: AsyncSession) -> User:
    user_dal = UserDAL(session)
    return await user_dal.get_user_by_username(username)


async def change_user_password(username: str, password: str, session: AsyncSession) -> None:
    user_dal = UserDAL(session)
    return await user_dal.change_user_password(username, password)
