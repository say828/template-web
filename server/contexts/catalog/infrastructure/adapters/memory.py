from contexts.catalog.domain import ProductRecord, ProductStatus, ProductSummary


class MemoryCatalogRepository:
    def __init__(self) -> None:
        self._products: dict[str, ProductRecord] = {}

    def initialize(self) -> None:
        return None

    def seed_products(self, products: list[ProductRecord]) -> None:
        for product in products:
            self._products[product.id] = product.model_copy(deep=True)

    def list_products(self) -> list[ProductRecord]:
        return [product.model_copy(deep=True) for product in self._products.values()]

    def list_summaries(self) -> list[ProductSummary]:
        return [
            ProductSummary(
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
            for product in self._products.values()
        ]

    def get_by_id(self, product_id: str) -> ProductRecord | None:
        product = self._products.get(product_id)
        return product.model_copy(deep=True) if product is not None else None

    def get_by_slug(self, slug: str) -> ProductRecord | None:
        normalized_slug = slug.casefold()
        for product in self._products.values():
            if product.slug.casefold() == normalized_slug:
                return product.model_copy(deep=True)
        return None

    def create_product(self, product: ProductRecord) -> ProductRecord:
        self._products[product.id] = product.model_copy(deep=True)
        return product.model_copy(deep=True)

    def update_product(self, product: ProductRecord) -> ProductRecord:
        self._products[product.id] = product.model_copy(deep=True)
        return product.model_copy(deep=True)

    def update_status(self, product_id: str, status: ProductStatus) -> ProductRecord | None:
        product = self._products.get(product_id)
        if product is None:
            return None
        updated = product.model_copy(update={"status": status})
        self._products[product_id] = updated
        return updated.model_copy(deep=True)
