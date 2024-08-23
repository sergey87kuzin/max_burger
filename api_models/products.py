from typing import Optional

from pydantic import BaseModel

from common_api_model import TunedModel

_all__ = (
    "ProductToCreate",
    "ProductToUpdate",
    "ProductToShow",
)


class ProductToCreate(BaseModel):
    name: str
    description: str
    price: float
    is_combo_product: bool
    category_id: int


class ProductToUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    is_combo_product: Optional[bool] = None
    category_id: Optional[int] = None


class ProductToShow(TunedModel):
    id: int
    name: str
    description: str
    price: float
    is_combo_product: bool
    category_id: int
    image: str | None = None
