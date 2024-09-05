"""test running migrations carts and orders

Revision ID: 52bba554a903
Revises: f46f2088563f
Create Date: 2024-09-05 19:59:49.582711

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '52bba554a903'
down_revision: Union[str, None] = 'f46f2088563f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
