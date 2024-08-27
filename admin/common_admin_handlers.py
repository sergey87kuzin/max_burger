from http import HTTPStatus

from fastapi import Response
from sqlalchemy.ext.asyncio import AsyncSession

from common_api_model import TunedModel
from db_models import Base
from pagination import PageParams, paginate, PagedResponseSchema

__all__ = (
    "create_new_object",
    "get_object",
    "update_object_by_id",
    "delete_object_by_id",
    "get_objects_list"
)


async def create_new_object(
        model,
        dal,
        response_model,
        body: dict,
        session: AsyncSession
) -> TunedModel:
    async with session.begin():
        current_dal = dal(model, session)
        created_object = await current_dal.create_object(body)
        return response_model.model_validate(created_object)


async def get_object(model, dal, response_model, object_id, session: AsyncSession) -> TunedModel:
    async with session.begin():
        current_dal = dal(model, session)
        found_object = await current_dal.get_object_by_id(object_id)
        return response_model.model_validate(found_object)


async def update_object_by_id(
        model,
        dal,
        response_model,
        object_id: int,
        body: dict,
        session: AsyncSession
) -> TunedModel:
    async with session.begin():
        current_dal = dal(model, session)
        updated_object = await current_dal.update_object(object_id, body)
        return response_model.model_validate(updated_object)


async def delete_object_by_id(
        model,
        dal,
        object_id: int,
        session: AsyncSession
):
    async with session.begin():
        current_dal = dal(model, session)
        await current_dal.delete_object(object_id)
        return Response(status_code=HTTPStatus.NO_CONTENT)


async def get_objects_list(
        model,
        dal,
        response_model,
        session: AsyncSession,
        page_params: PageParams,
        custom_filter
) -> PagedResponseSchema:
    async with (session.begin()):
        current_dal = dal(model, session)
        count, rows = await current_dal.get_full_objects_list(page_params, custom_filter)
        return await paginate(
            count=count,
            objects=rows,
            page_params=page_params,
            response_model=response_model
        )
