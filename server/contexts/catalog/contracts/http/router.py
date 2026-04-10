from fastapi import APIRouter, Depends, Query, status

from contexts.auth.contracts.http.dependencies import require_admin_user
from contexts.catalog.application import (
    create_product,
    get_product_or_404,
    list_product_summaries,
    update_product_or_404,
    update_product_status_or_404,
)
from contexts.catalog.domain import (
    CreateProductCommand,
    ProductDetail,
    ProductStatus,
    ProductSummary,
    UpdateProductCommand,
    UpdateProductStatusCommand,
)

router = APIRouter(prefix="/catalog", tags=["catalog"])


@router.get("/products", response_model=list[ProductSummary])
def list_products(
    product_status: ProductStatus | None = Query(default=None, alias="status"),
    category: str | None = Query(default=None),
    search: str | None = Query(default=None, alias="q"),
) -> list[ProductSummary]:
    return list_product_summaries(product_status=product_status, category=category, search=search)


@router.get("/products/{product_id}", response_model=ProductDetail)
def get_product(product_id: str) -> ProductDetail:
    return get_product_or_404(product_id)


@router.post("/products", response_model=ProductDetail, status_code=status.HTTP_201_CREATED)
def post_product(
    command: CreateProductCommand,
    _: object = Depends(require_admin_user),
) -> ProductDetail:
    return create_product(command)


@router.put("/products/{product_id}", response_model=ProductDetail)
def put_product(
    product_id: str,
    command: UpdateProductCommand,
    _: object = Depends(require_admin_user),
) -> ProductDetail:
    return update_product_or_404(product_id, command)


@router.patch("/products/{product_id}/status", response_model=ProductDetail)
def patch_product_status(
    product_id: str,
    command: UpdateProductStatusCommand,
    _: object = Depends(require_admin_user),
) -> ProductDetail:
    return update_product_status_or_404(product_id, command)
