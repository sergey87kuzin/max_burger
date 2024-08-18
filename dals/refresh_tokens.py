from sqlalchemy import select, update

from sqlalchemy.ext.asyncio import AsyncSession

from db_models import RefreshToken


class RefreshTokenDAL:
    def __init__(self, session: AsyncSession):
        self.db_session = session

    async def check_token_exists(self, token: str) -> bool:
        query = select(RefreshToken.id).where(RefreshToken.token == token)
        result = await self.db_session.execute(query)
        if result:
            return True
        return False

    async def create_refresh_token(self, token: str):
        self.db_session.add(RefreshToken(token=token))
        await self.db_session.flush()

    async def update_refresh_token(self, token, new_token):
        query = (
            update(RefreshToken)
            .where(RefreshToken.token == token)
            .values(token=new_token)
        )
        await self.db_session.execute(query)
