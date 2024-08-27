from typing import Optional

from fastapi_filter.contrib.sqlalchemy import Filter

from db_models import Product, Category, User

__all__ = (
    "ProductFilter",
    "CategoryFilter",
    "UserFilter",
)


class ProductFilter(Filter):
    name: Optional[str] = None
    category_id: Optional[int] = None
    price__gt: Optional[int] = None
    price__lte: Optional[int] = None
    custom_order_by: Optional[list[str]] = None
    custom_search: Optional[str] = None

    class Constants(Filter.Constants):
        model = Product
        ordering_field_name = "custom_order_by"
        search_field_name = "custom_search"
        search_model_fields = ["name", "description"]


class CategoryFilter(Filter):
    name: Optional[str] = None
    is_active: Optional[bool] = None

    class Constants(Filter.Constants):
        model = Category


class UserFilter(Filter):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None
    phone: Optional[str] = None
    custom_order_by: Optional[list[str]] = None
    custom_search: Optional[str] = None

    class Constants(Filter.Constants):
        model = User
        ordering_field_name = "custom_order_by"
        search_field_name = "custom_search"
        search_model_fields = ["username", "first_name", "last_name", "phone"]
