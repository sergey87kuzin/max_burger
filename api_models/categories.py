from typing import Optional

from pydantic import BaseModel

from common_api_model import TunedModel

__all__ = (
    "CategoryToCreate",
    "CategoryToUpdate",
    "CategoryToShow"
)


class CategoryToCreate(BaseModel):
    name: str
    is_active: bool


class CategoryToUpdate(BaseModel):
    name: Optional[str] = None
    is_active: Optional[bool] = None


class CategoryToShow(TunedModel):
    id: int
    name: str
    is_active: bool
    cover: str | None = None
