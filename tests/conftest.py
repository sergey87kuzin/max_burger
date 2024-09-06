import asyncio
from typing import Any
from typing import Generator

import alembic.config
import alembic.command
import asyncpg
import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient

from database_interaction import get_db
from db_models import Category, User, Product, Cart, CartItem
from global_constants import PaymentStatus
from hashing import Hasher
from main import app
from settings import TEST_DATABASE_URL, TEST_PASSWORD

CLEAN_TABLES = [
    "users",
    "categories",
    "products",
    "carts",
    "cart_items",
    "orders",
    "order_items",
]


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


# @pytest.fixture(scope="session", autouse=True)
# def a_run_migrations():
    # config = alembic.config.Config("alembic.ini")
    # alembic.command.revision(config, autogenerate=True, message="test running migrations carts and orders")
    # alembic.command.upgrade(config, "head")


@pytest.fixture(scope="session")
async def async_session_test():
    engine = create_async_engine(TEST_DATABASE_URL, future=True, echo=True)
    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    yield async_session


@pytest.fixture(scope="function", autouse=True)
async def clean_tables(async_session_test):
    """Clean data in all tables before running test function"""
    async with async_session_test() as session:
        async with session.begin():
            for table_for_cleaning in CLEAN_TABLES:
                await session.execute(text(f"TRUNCATE TABLE {table_for_cleaning} CASCADE;"))


async def _get_test_db():
    try:
        # create async engine for interaction with database
        test_engine = create_async_engine(
            TEST_DATABASE_URL, future=True, echo=True
        )

        # create session for the interaction with database
        test_async_session = sessionmaker(
            test_engine, expire_on_commit=False, class_=AsyncSession
        )
        yield test_async_session()
    finally:
        pass


@pytest.fixture(scope="function")
async def client() -> Generator[TestClient, Any, None]:
    """
    Create a new FastAPI TestClient that uses the `db_session` fixture to override
    the `get_db` dependency that is injected into routes.
    """

    app.dependency_overrides[get_db] = _get_test_db
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="session")
async def asyncpg_pool():
    pool = await asyncpg.create_pool(
        "".join(TEST_DATABASE_URL.split("+asyncpg"))
    )
    yield pool
    pool.close()


@pytest.fixture
async def get_user_from_database(async_session_test):
    async def get_user_from_database_by_username(username: str):
        async with async_session_test() as session:
            user_row = await session.execute(
                text("SELECT * FROM users WHERE username = :un;"), {"un": username}
            )
            if user := user_row.fetchall()[0]:
                return user

    return get_user_from_database_by_username


@pytest.fixture
async def create_category(async_session_test):
    async with async_session_test() as session:
        new_category = Category(
            name="Test Category",
            cover="some_cover",
            is_active=True
        )
        session.add(new_category)
        await session.commit()
        return new_category


@pytest.fixture
async def create_admin(async_session_test):
    async def create_admin_in_database(username: str, password: str):
        password = Hasher.get_password_hash(password)
        new_admin = User(
            username=username,
            first_name="Grey",
            last_name="Tres",
            phone="+79117973895",
            is_active=True,
            is_staff=True,
            is_admin=True,
            password=password
        )
        async with async_session_test() as session:
            session.add(new_admin)
            await session.commit()
        return new_admin

    return create_admin_in_database


@pytest.fixture
async def create_user_cart(async_session_test):
    async def create_user_cart_in_database(username: str, category_name: str, product_name: str):
        async with async_session_test() as session:
            new_category = Category(
                name=category_name,
                is_active=True,
                # cover="some cover"
            )
            session.add(new_category)
            await session.flush()

            new_product = Product(
                name=product_name,
                is_combo_product=False,
                is_active=True,
                price=100500,
                category_id=new_category.id,
                description="some description",
                image="some_image.jpg",
            )

            session.add(new_product)
            await session.flush()

            password = Hasher.get_password_hash(TEST_PASSWORD)
            user = User(
                username=username,
                first_name="Grey",
                last_name="Tres",
                phone="+79117973895",
                is_active=True,
                is_staff=False,
                is_admin=False,
                password=password
            )

            session.add(user)
            await session.flush()

            cart = Cart(
                products_count=1,
                user_id=user.id,
                total_price=new_product.price,
                payment_status=PaymentStatus.NOT_PAID
            )
            session.add(cart)
            await session.flush()

            cart_product = CartItem(
                cart_id=cart.id,
                product_id=new_product.id,
                count=1,
                position_price=new_product.price,
            )
            session.add(cart_product)
            await session.commit()
        return cart
    return create_user_cart_in_database


# def create_test_auth_headers_for_user(email: str) -> dict[str, str]:
#     access_token = create_access_token(
#         data={"sub": email},
#         expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
#     )
#     return {"Authorization": f"Bearer {access_token}"}
