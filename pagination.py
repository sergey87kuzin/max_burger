from typing import Generic, List, TypeVar
from pydantic import BaseModel, conint
from sqlalchemy import select


class PageParams(BaseModel):
    """ Request query params for paginated API. """
    page: conint(ge=1) = 1
    size: conint(ge=1, le=100) = 10

    def get_params(self):
        return dict(page=self.page, size=self.size)


T = TypeVar("T")


class PagedResponseSchema(BaseModel, Generic[T]):
    """Response schema for any paged API."""

    total: int
    page: int
    size: int
    results: List[T]


async def paginate(page_params: PageParams, query, response_model) -> PagedResponseSchema[T]:
    """Paginate the query."""

    paginated_query = await query.offset((page_params.page - 1) * page_params.size).limit(page_params.size).all()

    return PagedResponseSchema(
        total=query.count(),
        page=page_params.page,
        size=page_params.size,
        results=[response_model.from_orm(item) for item in paginated_query],
    )
