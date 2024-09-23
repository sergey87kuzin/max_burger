from typing import Generic, List, TypeVar
from pydantic import BaseModel, conint


class PageParams(BaseModel):
    """ Request query params for paginated API. """
    page: conint(ge=1) = 1
    size: conint(ge=1, le=100) = 10

    def get_params(self):
        return dict(page=self.page, size=self.size)


T = TypeVar("T")


class PagedResponseSchema(BaseModel, Generic[T]):
    """Response schema for any paged API."""

    objects_count: int
    page: int
    size: int
    objects: List[T]


async def paginate(count: int, objects: list, page_params: PageParams, response_model) -> PagedResponseSchema[T]:
    """Paginate the query."""

    return PagedResponseSchema(
        objects_count=count,
        page=page_params.page,
        size=page_params.size,
        objects=[response_model.model_validate(item) for item in objects],
    )
