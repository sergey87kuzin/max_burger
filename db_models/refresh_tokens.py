from sqlalchemy.orm import Mapped

from db_models import Base, intpk, str_256

__all__ = ['RefreshToken']


class RefreshToken(Base):
    __tablename__ = 'refresh_tokens'

    id: Mapped[intpk]
    token: Mapped[str_256]
