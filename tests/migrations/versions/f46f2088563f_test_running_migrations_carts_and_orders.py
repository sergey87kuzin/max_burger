"""test running migrations carts and orders

Revision ID: f46f2088563f
Revises: d4cc7cd3a895
Create Date: 2024-09-05 19:46:47.369993

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils

from global_constants import PaymentStatus, DeliveryType, PaymentType

# revision identifiers, used by Alembic.
revision: str = 'f46f2088563f'
down_revision: Union[str, None] = 'd4cc7cd3a895'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('carts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('total_price', sa.Float(), nullable=False),
    sa.Column('products_count', sa.Integer(), nullable=False),
    sa.Column(
        'payment_status',
        sqlalchemy_utils.types.choice.ChoiceType(choices=PaymentStatus, impl=sa.String(length=32)),
        nullable=True
    ),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('orders',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('total_price', sa.Float(), nullable=False),
    sa.Column('delivery_price', sa.Integer(), nullable=False),
    sa.Column(
        'delivery_type',
        sqlalchemy_utils.types.choice.ChoiceType(choices=DeliveryType, impl=sa.String(length=16)),
        nullable=True
    ),
    sa.Column(
        'payment_status',
        sqlalchemy_utils.types.choice.ChoiceType(choices=PaymentStatus, impl=sa.String(length=32)),
        nullable=True
    ),
    sa.Column('payment_url', sa.String(length=128), nullable=True),
    sa.Column(
        'payment_type',
        sqlalchemy_utils.types.choice.ChoiceType(choices=PaymentType, impl=sa.String(length=32)),
        nullable=True
    ),
    sa.Column('city', sa.String(length=64), nullable=True),
    sa.Column('street', sa.String(length=64), nullable=True),
    sa.Column('house_number', sa.String(length=64), nullable=True),
    sa.Column('apartment', sa.String(length=64), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('cart_items',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('position_price', sa.Float(), nullable=False),
    sa.Column('count', sa.Integer(), nullable=False),
    sa.Column('cart_id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['cart_id'], ['carts.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('order_items',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('position_price', sa.Float(), nullable=False),
    sa.Column('count', sa.Integer(), nullable=False),
    sa.Column('order_id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['order_id'], ['orders.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('order_items')
    op.drop_table('cart_items')
    op.drop_table('orders')
    op.drop_table('carts')
    # ### end Alembic commands ###
