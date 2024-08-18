import datetime
from typing import Annotated

from sqlalchemy import DateTime, Integer, String, text  # noqa
from sqlalchemy.orm import DeclarativeBase, mapped_column

str_2048 = Annotated[str, 2048]
str_256 = Annotated[str, 256]
str_128 = Annotated[str, 128]
str_512 = Annotated[str, 512]
str_1024 = Annotated[str, 1024]
str_8 = Annotated[str, 8]
str_16 = Annotated[str, 16]
str_32 = Annotated[str, 32]
str_64 = Annotated[str, 64]
intpk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[
    datetime.datetime,
    mapped_column(default=datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None))
]
# created_at = Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]


class Base(DeclarativeBase):
    type_annotation_map = {
        str_2048: String(2048),
        str_256: String(256),
        str_128: String(128),
        str_512: String(512),
        str_1024: String(1024),
        str_8: String(8),
        str_16: String(16),
        str_32: String(32),
        str_64: String(64),
        intpk: Integer,
        created_at: DateTime,
    }


from .address import *  # noqa
from .cart import *  # noqa
from .categories import *  # noqa
from .orders import *  # noqa
from .products import *  # noqa
from .refresh_tokens import *  # noqa
from .users import *  # noqa
