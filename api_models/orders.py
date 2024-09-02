from typing import Optional

from pydantic import BaseModel

__all__ = (
    "OrderToCreate",
)


class OrderToCreate(BaseModel):
    user_id: int
    city: Optional[str] = None
    street: Optional[str] = None
    house_number: Optional[str] = None
    apartment: Optional[str] = None
