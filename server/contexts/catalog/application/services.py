from datetime import datetime, timezone
from functools import lru_cache

from fastapi import HTTPException, status as http_status

from contexts.catalog.domain import (
    CreateProductCommand,
    ProductDetail,
    ProductRecord,
    ProductStatus,
    ProductSummary,
    UpdateProductCommand,
    UpdateProductStatusCommand,
)
from contexts.catalog.infrastructure import get_catalog_repository
from data.bootstrap_loader import load_bootstrap_json


def list_product_summaries(
    product_status: ProductStatus | None = None,
    category: str | None = None,
    search: str | None = None,
) -> list[ProductSummary]:
    prepare_catalog_store()
    repository = get_catalog_repository()
    products = repository.list_products()

    if product_status is not None:
        products = [product for product in products if product.status == product_status]
    if category is not None:
        normalized_category = category.strip().casefold()
        products = [product for product in products if product.category.casefold() == normalized_category]
    if search is not None:
        normalized_search = search.strip().casefold()
        products = [
            product
            for product in products
            if normalized_search
            in " ".join([product.name, product.brand, product.category, product.slug, *product.tags]).casefold()
        ]

    return [_to_summary(product) for product in products]


def get_product_or_404(product_id: str) -> ProductDetail:
    prepare_catalog_store()
    repository = get_catalog_repository()
    product = repository.get_by_id(product_id)
    if product is None:
        raise HTTPException(status_code=http_status.HTTP_404_NOT_FOUND, detail="Catalog product not found")
    return ProductDetail(**product.model_dump())


def create_product(command: CreateProductCommand) -> ProductDetail:
    prepare_catalog_store()
    repository = get_catalog_repository()
    if repository.get_by_slug(command.slug) is not None:
        raise HTTPException(status_code=http_status.HTTP_409_CONFLICT, detail="Catalog product slug already exists")

    next_id = _next_product_id(repository.list_products())
    timestamp = _now_iso()
    product = ProductRecord(
        id=next_id,
        slug=command.slug,
        name=command.name,
        brand=command.brand,
        category=command.category,
        status=command.status,
        short_description=command.short_description,
        description=command.description,
        hero_image=command.hero_image,
        gallery=command.gallery,
        price=command.price,
        compare_at_price=command.compare_at_price,
        tags=command.tags,
        attributes=command.attributes,
        variants=command.variants,
        created_at=timestamp,
        updated_at=timestamp,
    )
    return ProductDetail(**repository.create_product(product).model_dump())


def update_product_or_404(product_id: str, command: UpdateProductCommand) -> ProductDetail:
    prepare_catalog_store()
    repository = get_catalog_repository()
    current = repository.get_by_id(product_id)
    if current is None:
        raise HTTPException(status_code=http_status.HTTP_404_NOT_FOUND, detail="Catalog product not found")

    updates = command.model_dump(exclude_none=True, exclude_unset=True)
    if not updates:
        raise HTTPException(status_code=http_status.HTTP_400_BAD_REQUEST, detail="No catalog product fields provided")

    if "slug" in updates:
        existing = repository.get_by_slug(updates["slug"])
        if existing is not None and existing.id != product_id:
            raise HTTPException(status_code=http_status.HTTP_409_CONFLICT, detail="Catalog product slug already exists")

    updated = current.model_copy(update={**updates, "updated_at": _now_iso()})
    return ProductDetail(**repository.update_product(updated).model_dump())


def update_product_status_or_404(product_id: str, command: UpdateProductStatusCommand) -> ProductDetail:
    prepare_catalog_store()
    repository = get_catalog_repository()
    current = repository.get_by_id(product_id)
    if current is None:
        raise HTTPException(status_code=http_status.HTTP_404_NOT_FOUND, detail="Catalog product not found")
    updated = current.model_copy(update={"status": command.status, "updated_at": _now_iso()})
    return ProductDetail(**repository.update_product(updated).model_dump())


def prepare_catalog_store() -> None:
    _seed_catalog_store()


@lru_cache
def _seed_catalog_store() -> None:
    repository = get_catalog_repository()
    repository.initialize()
    records = [ProductRecord(**entry) for entry in load_bootstrap_json("catalog_products.json")]
    repository.seed_products(records)


def _to_summary(product: ProductRecord) -> ProductSummary:
    return ProductSummary(
        id=product.id,
        slug=product.slug,
        name=product.name,
        brand=product.brand,
        category=product.category,
        status=product.status,
        short_description=product.short_description,
        hero_image=product.hero_image,
        price=product.price,
        compare_at_price=product.compare_at_price,
        tags=product.tags,
        variant_count=len(product.variants),
    )


def _next_product_id(products: list[ProductRecord]) -> str:
    max_sequence = 1000
    for product in products:
        try:
            max_sequence = max(max_sequence, int(product.id.split("-")[-1]))
        except ValueError:
            continue
    return f"prd-{max_sequence + 1}"


def _now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()
