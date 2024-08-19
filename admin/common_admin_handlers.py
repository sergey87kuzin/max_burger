from http import HTTPStatus

from fastapi import Response
from sqlalchemy.ext.asyncio import AsyncSession

__all__ = (
    "create_new_object",
    "get_object",
    "update_object_by_id",
    "delete_object_by_id",
    "get_objects_list"
)


async def create_new_object(model, dal, response_model, body: dict, session: AsyncSession):
    current_dal = dal(model, session)
    created_object = await current_dal.create_object(body)
    return response_model.model_validate(created_object, from_attributes=True)


async def get_object(model, dal, response_model, object_id, session: AsyncSession):
    current_dal = dal(model, session)
    created_object = await current_dal.get_object_by_id(object_id)
    return response_model.model_validate(created_object, from_attributes=True)


async def update_object_by_id(model, dal, response_model, object_id: int, body: dict, session: AsyncSession):
    current_dal = dal(model, session)
    created_object = await current_dal.update_object(object_id, body)
    return response_model.model_validate(created_object, from_attributes=True)


async def delete_object_by_id(model, dal, object_id, session: AsyncSession):
    current_dal = dal(model, session)
    await current_dal.delete_object(object_id)
    return Response(status_code=HTTPStatus.NO_CONTENT)


async def get_objects_list(model, dal, response_model, session: AsyncSession):
    current_dal = dal(model, session)
    result = await current_dal.get_full_objects_list()
    return [response_model.model_validate(row, from_attributes=True) for row in result]
