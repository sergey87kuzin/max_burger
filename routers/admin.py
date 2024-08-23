from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from admin import get_objects_list, CommonAdminDAL, get_object, update_object_by_id, delete_object_by_id, \
    create_new_object
from api_models import UserToShow, UserToCreate, UserToUpdate, ProductToShow, ProductToUpdate, ProductToCreate, \
    CategoryToCreate, CategoryToShow, CategoryToUpdate
from database_interaction import get_db
from db_models import User, Product, Category

admin_router = APIRouter()


# USERS ADMIN
@admin_router.post("/users/")
async def admin_create_user(user: UserToCreate, session: AsyncSession = Depends(get_db)):
    return await create_new_object(
        model=User,
        dal=CommonAdminDAL,
        response_model=UserToShow,
        body=user.dict(),
        session=session
    )


@admin_router.get("/users/list/")
async def admin_list_users(session: AsyncSession = Depends(get_db)):
    return await get_objects_list(
        model=User,
        dal=CommonAdminDAL,
        response_model=UserToShow,
        session=session
    )


@admin_router.get("/users/{user_id}")
async def admin_get_user(user_id: int, session: AsyncSession = Depends(get_db)):
    return await get_object(
        model=User,
        dal=CommonAdminDAL,
        response_model=UserToShow,
        object_id=user_id,
        session=session
    )


@admin_router.post("/users/{user_id}")
async def admin_update_user(user_id: int, user_data: UserToUpdate, session: AsyncSession = Depends(get_db)):
    return await update_object_by_id(
        model=User,
        dal=CommonAdminDAL,
        object_id=user_id,
        body=user_data.dict(),
        response_model=UserToShow,
        session=session
    )


@admin_router.delete("/users/{user_id}")
async def admin_delete_user(user_id: int, session: AsyncSession = Depends(get_db)):
    return await delete_object_by_id(
        model=User,
        dal=CommonAdminDAL,
        object_id=user_id,
        session=session
    )


# PRODUCTS ADMIN
@admin_router.post("/products/")
async def admin_create_product(product: ProductToCreate, session: AsyncSession = Depends(get_db)):
    return await create_new_object(
        model=Product,
        dal=CommonAdminDAL,
        response_model=ProductToShow,
        body=product.dict(),
        session=session
    )


@admin_router.get("/products/list/")
async def admin_list_products(session: AsyncSession = Depends(get_db)):
    return await get_objects_list(
        model=Product,
        dal=CommonAdminDAL,
        response_model=ProductToShow,
        session=session
    )


@admin_router.get("/products/{product_id}/")
async def admin_get_product(product_id: int, session: AsyncSession = Depends(get_db)):
    return await get_object(
        model=Product,
        dal=CommonAdminDAL,
        response_model=ProductToShow,
        object_id=product_id,
        session=session
    )


@admin_router.post("/products/{product_id}/")
async def admin_update_product(
        product_id: int,
        product_data: ProductToUpdate,
        session: AsyncSession = Depends(get_db)
):
    return await update_object_by_id(
        model=Product,
        dal=CommonAdminDAL,
        object_id=product_id,
        body=product_data.dict(),
        response_model=ProductToShow,
        session=session
    )


@admin_router.delete("/products/{product_id}/")
async def admin_delete_product(product_id: int, session: AsyncSession = Depends(get_db)):
    return await delete_object_by_id(
        model=Product,
        dal=CommonAdminDAL,
        object_id=product_id,
        session=session
    )


# CATEGORY ADMIN
@admin_router.post("/categories/")
async def admin_create_category(category: CategoryToCreate, session: AsyncSession = Depends(get_db)):
    return await create_new_object(
        model=Category,
        dal=CommonAdminDAL,
        response_model=CategoryToShow,
        body=category.dict(),
        session=session
    )


@admin_router.get("/categories/list/")
async def admin_list_categories(session: AsyncSession = Depends(get_db)):
    return await get_objects_list(
        model=Category,
        dal=CommonAdminDAL,
        response_model=CategoryToShow,
        session=session
    )


@admin_router.get("/categories/{category_id}/")
async def admin_get_category(category_id: int, session: AsyncSession = Depends(get_db)):
    return await get_object(
        model=Category,
        dal=CommonAdminDAL,
        response_model=CategoryToShow,
        object_id=category_id,
        session=session
    )


@admin_router.post("/categories/{category_id}/")
async def admin_update_category(
        category_id: int,
        category_data: CategoryToUpdate,
        session: AsyncSession = Depends(get_db)
):
    return await update_object_by_id(
        model=Category,
        dal=CommonAdminDAL,
        object_id=category_id,
        body=category_data.dict(),
        response_model=CategoryToShow,
        session=session
    )


@admin_router.delete("/categories/{category_id}/")
async def admin_delete_category(category_id: int, session: AsyncSession = Depends(get_db)):
    return await delete_object_by_id(
        model=Category,
        dal=CommonAdminDAL,
        object_id=category_id,
        session=session
    )
