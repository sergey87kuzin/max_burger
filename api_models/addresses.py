from typing import Optional

from pydantic import BaseModel

from common_api_model import TunedModel

__all__ = (
    "AddressToCreate",
    "AddressToUpdate",
    "AddressToShow"
)


class AddressToCreate(BaseModel):
    name: str
    postal_code: str
    city: str
    street: str
    house_number: str
    apartment: str
    user_id: Optional[int] = None


class AddressToUpdate(BaseModel):
    name: Optional[str] = None
    postal_code: Optional[str] = None
    city: Optional[str] = None
    street: Optional[str] = None
    house_number: Optional[str] = None
    apartment: Optional[str] = None


class AddressToShow(TunedModel):
    id: int
    name: str
    postal_code: str
    city: str
    street: str
    house_number: str
    apartment: str
