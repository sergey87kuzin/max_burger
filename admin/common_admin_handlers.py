from http import HTTPStatus
from fastapi import HTTPException

from fastapi import Response, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

__all__ = (
    "create_new_object",
    "get_object",
    "update_object_by_id",
    "delete_object_by_id",
    "get_objects_list"
)

from pagination import PageParams, paginate


async def create_new_object(model, dal, response_model, body: dict, session: AsyncSession):
    async with session.begin():
        current_dal = dal(model, session)
        created_object = await current_dal.create_object(body)
        return response_model.model_validate(created_object, from_attributes=True)


async def get_object(model, dal, response_model, object_id, session: AsyncSession):
    async with session.begin():
        current_dal = dal(model, session)
        found_object = await current_dal.get_object_by_id(object_id)
        return response_model.model_validate(found_object, from_attributes=True)


async def update_object_by_id(model, dal, response_model, object_id: int, body: dict, session: AsyncSession):
    async with session.begin():
        current_dal = dal(model, session)
        updated_object = await current_dal.update_object(object_id, body)
        return response_model.model_validate(updated_object, from_attributes=True)


async def delete_object_by_id(model, dal, object_id, session: AsyncSession):
    async with session.begin():
        current_dal = dal(model, session)
        await current_dal.delete_object(object_id)
        return Response(status_code=HTTPStatus.NO_CONTENT)


async def get_objects_list(
        model,
        dal,
        response_model,
        session: AsyncSession,
        page_params: PageParams
):
    async with (session.begin()):
        current_dal = dal(model, session)
        count, rows = await current_dal.get_full_objects_list(page_params)
        # return await paginate(page_params, result, response_model)
        return {
            "objects_count": count,
            "objects": [response_model.model_validate(row, from_attributes=True) for row in rows]
        }
