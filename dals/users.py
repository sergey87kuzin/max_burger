from http import HTTPStatus

from fastapi import HTTPException

from sqlalchemy import select, and_, update, func
from sqlalchemy.ext.asyncio import AsyncSession

from api_models import UserToCreate, UserToUpdate, UserToUpdateProfile
from db_models import User
from hashing import Hasher

__all__ = (
    "UserDAL",
)


class UserDAL:
    def __init__(self, session: AsyncSession):
        self.db_session = session

    async def create_user(self, user_data: UserToCreate) -> User:
        new_user = User(**user_data.dict())
        self.db_session.add(new_user)
        await self.db_session.commit()
        return new_user

    async def get_user_by_username(self, username: str) -> User:
        query = (
            select(User)
            .where(and_(
                func.lower(User.username) == func.lower(username),
                User.is_active == True
            ))
        )
        result = await self.db_session.execute(query)
        if not result:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )
        return result.scalars().first()

    async def change_user_password(self, username: str, new_password: str) -> None:
        query = (
            update(User)
            .where(and_(func.lower(User.username) == username, User.is_active == True))
            .values({"password": Hasher.get_password_hash(new_password)})
        )
        await self.db_session.execute(query)

    async def update_user(self, user_id: int, user_data: UserToUpdateProfile) -> User:
        update_data = {key: value for key, value in user_data.model_dump().items() if value is not None}
        query = update(User).where(User.id == user_id).values(update_data).returning(User)
        result = await self.db_session.execute(query)
        user = result.scalar()
        if not user:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="User not found"
            )
        return user
