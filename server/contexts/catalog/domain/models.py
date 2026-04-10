from typing import Literal, TypeAlias

from pydantic import BaseModel, Field

ProductStatus = Literal["draft", "active", "archived"]
CatalogProductStatus: TypeAlias = ProductStatus


class Money(BaseModel):
    amount: int = Field(ge=0)
    currency: str = Field(min_length=3, max_length=3)


class MediaAsset(BaseModel):
    url: str = Field(min_length=1)
    alt: str = Field(min_length=1)


class ProductAttribute(BaseModel):
    name: str = Field(min_length=1)
    value: str = Field(min_length=1)


class ProductVariant(BaseModel):
    sku: str = Field(min_length=1)
    name: str = Field(min_length=1)
    option_values: list[str] = Field(min_length=1)


class ProductRecord(BaseModel):
    id: str
    slug: str
    name: str
    brand: str
    category: str
    status: ProductStatus
    short_description: str
    description: str
    hero_image: MediaAsset
    gallery: list[MediaAsset] = Field(default_factory=list)
    price: Money
    compare_at_price: Money | None = None
    tags: list[str] = Field(default_factory=list)
    attributes: list[ProductAttribute] = Field(default_factory=list)
    variants: list[ProductVariant] = Field(min_length=1)
    created_at: str
    updated_at: str


class ProductSummary(BaseModel):
    id: str
    slug: str
    name: str
    brand: str
    category: str
    status: ProductStatus
    short_description: str
    hero_image: MediaAsset
    price: Money
    compare_at_price: Money | None = None
    tags: list[str] = Field(default_factory=list)
    variant_count: int


class ProductDetail(ProductRecord):
    pass


class CreateProductCommand(BaseModel):
    slug: str = Field(min_length=1)
    name: str = Field(min_length=1)
    brand: str = Field(min_length=1)
    category: str = Field(min_length=1)
    status: ProductStatus = "draft"
    short_description: str = Field(min_length=1)
    description: str = Field(min_length=1)
    hero_image: MediaAsset
    gallery: list[MediaAsset] = Field(default_factory=list)
    price: Money
    compare_at_price: Money | None = None
    tags: list[str] = Field(default_factory=list)
    attributes: list[ProductAttribute] = Field(default_factory=list)
    variants: list[ProductVariant] = Field(min_length=1)


class UpdateProductCommand(BaseModel):
    slug: str | None = Field(default=None, min_length=1)
    name: str | None = Field(default=None, min_length=1)
    brand: str | None = Field(default=None, min_length=1)
    category: str | None = Field(default=None, min_length=1)
    short_description: str | None = Field(default=None, min_length=1)
    description: str | None = Field(default=None, min_length=1)
    hero_image: MediaAsset | None = None
    gallery: list[MediaAsset] | None = None
    price: Money | None = None
    compare_at_price: Money | None = None
    tags: list[str] | None = None
    attributes: list[ProductAttribute] | None = None
    variants: list[ProductVariant] | None = Field(default=None, min_length=1)


class UpdateProductStatusCommand(BaseModel):
    status: ProductStatus


CatalogMoney = Money
CatalogMedia = MediaAsset
CatalogProductRecord = ProductRecord
CatalogProductSummary = ProductSummary
CatalogProductDetail = ProductDetail
CatalogProductCreateCommand = CreateProductCommand
CatalogProductUpdateCommand = UpdateProductCommand
CatalogProductStatusCommand = UpdateProductStatusCommand
