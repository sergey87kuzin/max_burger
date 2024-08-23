from http import HTTPStatus

from fastapi import HTTPException, Response
from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

__all__ = (
    "CommonAdminDAL",
)


class CommonAdminDAL:
    def __init__(self, model, session: AsyncSession):
        """model - модель, над которой планируем производить действия"""
        self.model = model
        self.db_session = session

    async def get_full_objects_list(self):
        rows = await self.db_session.execute(select(self.model))
        return rows.unique().scalars().all()

    async def get_object_by_id(self, object_id: int):
        query = (
            select(self.model)
            .where(self.model.id == object_id)
        )
        result = await self.db_session.execute(query)
        if not result:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="Объект не найден"
            )
        return result.scalars().first()

    async def create_object(self, data: dict):
        new_object = self.model(**data)
        self.db_session.add(new_object)
        await self.db_session.flush()
        await self.db_session.commit()
        return new_object

    async def update_object(self, object_id: int, data: dict):
        update_data = {key: value for key, value in data.items() if value is not None}
        query = (
            update(self.model)
            .where(self.model.id == object_id)
            .values(**update_data)
            .returning(self.model)
        )
        result = await self.db_session.execute(query)
        if not result:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="Объект не изменен"
            )
        await self.db_session.commit()
        return result.scalars().first()

    async def delete_object(self, object_id: int):
        query = (
            delete(self.model)
            .where(self.model.id == object_id)
        )
        await self.db_session.execute(query)
        await self.db_session.commit()
        return Response(status_code=HTTPStatus.NO_CONTENT)
