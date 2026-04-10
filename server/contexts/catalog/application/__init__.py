from .services import (
    create_product,
    get_product_or_404,
    list_product_summaries,
    prepare_catalog_store,
    update_product_or_404,
    update_product_status_or_404,
)

create_catalog_product = create_product
get_catalog_product_or_404 = get_product_or_404
list_catalog_products = list_product_summaries
update_catalog_product = update_product_or_404
update_catalog_product_status = update_product_status_or_404

__all__ = [
    "create_catalog_product",
    "create_product",
    "get_catalog_product_or_404",
    "get_product_or_404",
    "list_catalog_products",
    "list_product_summaries",
    "prepare_catalog_store",
    "update_catalog_product",
    "update_catalog_product_status",
    "update_product_or_404",
    "update_product_status_or_404",
]
