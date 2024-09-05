from typing import Optional

from pydantic import BaseModel, field_validator

__all__ = (
    "OrderToCreate",
    "OrderToShow"
)

from api_models.products import ProductToShow
from common_api_model import TunedModel
from global_constants import PaymentType


class OrderToCreate(BaseModel):
    user_id: int
    city: Optional[str] = None
    street: Optional[str] = None
    house_number: Optional[str] = None
    apartment: Optional[str] = None
    payment_type: PaymentType

    @field_validator("payment_type", mode="before")
    def set_name(cls, value):
        return value or PaymentType.CASH


class OrderProductToShow(TunedModel):
    position_price: float
    count: int
    product: ProductToShow


class OrderToShow(TunedModel):
    id: int
    payment_url: Optional[str] = None
    payment_status: str
    products: list[OrderProductToShow]
