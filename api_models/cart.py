from typing import List

from pydantic import BaseModel

from api_models import ProductToShow
from common_api_model import TunedModel


class CartItemToShow(TunedModel):
    id: int
    product: ProductToShow
    count: int
    position_price: float


class CartToShow(TunedModel):
    id: int | None = None
    products: List[CartItemToShow]
    total_price: float
    products_count: int


class CartProductData(BaseModel):
    user_id: int
    product_id: int
    quantity: int


class CartGetInfo(BaseModel):
    user_id: int
