from typing import Optional

from pydantic import BaseModel

__all__ = (
    "OrderToCreate",
    "OrderToShow"
)

from common_api_model import TunedModel


class OrderToCreate(BaseModel):
    user_id: int
    city: Optional[str] = None
    street: Optional[str] = None
    house_number: Optional[str] = None
    apartment: Optional[str] = None


class OrderToShow(TunedModel):
    id: int
    payment_url: Optional[str] = None
    payment_status: str
