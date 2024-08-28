from typing import Optional

from fastapi_filter.contrib.sqlalchemy import Filter

from db_models import Product

__all__ = (
    "CatalogProductFilter",
)


class CatalogProductFilter(Filter):
    name: Optional[str] = None
    category_id: Optional[int] = None
    custom_search: Optional[str] = None

    class Constants(Filter.Constants):
        model = Product
        search_field_name = "custom_search"
        search_model_fields = ["name", "description"]
