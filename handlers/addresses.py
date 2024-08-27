from sqlalchemy.ext.asyncio import AsyncSession

from api_models.addresses import AddressToShow, AddressToUpdate, AddressToCreate

__all__ = (
    "get_user_address",
    "update_user_address",
    "create_user_address",
)

from dals.addresses import AddressDAL


async def get_user_address(user_id: int, session: AsyncSession) -> AddressToShow:
    async with session.begin():
        address_dal = AddressDAL(session)
        address = await address_dal.get_user_address(user_id)
        return AddressToShow.model_validate(address)


async def update_user_address(user_id: int, address_data: AddressToUpdate, session: AsyncSession) -> AddressToShow:
    async with session.begin():
        address_dal = AddressDAL(session)
        address = await address_dal.update_user_address(user_id, address_data)
        return AddressToShow.model_validate(address)


async def create_user_address(address_data: AddressToCreate, session: AsyncSession) -> AddressToShow:
    async with session.begin():
        address_dal = AddressDAL(session)
        address = await address_dal.create_user_address(address_data)
        return AddressToShow.model_validate(address)
