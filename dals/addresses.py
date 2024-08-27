from http import HTTPStatus

from fastapi import HTTPException

from sqlalchemy import select, and_, update, func
from sqlalchemy.ext.asyncio import AsyncSession

from api_models import UserToCreate
from api_models.addresses import AddressToShow, AddressToUpdate, AddressToCreate
from db_models import User, Address
from hashing import Hasher

__all__ = (
    "AddressDAL",
)


class AddressDAL:
    def __init__(self, session: AsyncSession):
        self.db_session = session

    async def get_user_address(self, user_id: int) -> Address:
        address_query = select(Address).where(Address.user_id == user_id)
        addresses = await self.db_session.execute(address_query)
        if not addresses:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f"У данного пользователя нет соханенных адресов"
            )
        return addresses.scalars().first()

    async def update_user_address(self, user_id: int, address: AddressToUpdate) -> Address:
        update_data = {key: value for key, value in address.model_dump().items() if value is not None}
        update_query = (
            update(Address)
            .where(Address.user_id == user_id)
            .values(update_data)
            .returning(Address)
        )
        address = await self.db_session.execute(update_query)
        if not address:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="У данного пользователя нет сохраненного адреса"
            )
        return address.scalars().first()

    async def create_user_address(self, address: AddressToCreate) -> Address:
        new_address = Address(**address.model_dump())
        self.db_session.add(new_address)
        await self.db_session.flush()
        return new_address
