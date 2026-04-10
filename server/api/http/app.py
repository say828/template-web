from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.http.router import api_router
from config import get_settings
from contexts.alerts.application import prepare_alert_store
from contexts.auth.application import prepare_auth_store
from contexts.catalog.application import prepare_catalog_store
from contexts.fulfillment.application import prepare_fulfillment_store
from contexts.inventory.application import prepare_inventory_store
from contexts.orders.application import prepare_order_store
from contexts.shipping.application import prepare_shipping_store
from contexts.support.application import prepare_support_store
from contexts.user.application import prepare_user_store
from shared.application import health_response

settings = get_settings()


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    prepare_alert_store()
    prepare_auth_store()
    prepare_catalog_store()
    prepare_fulfillment_store()
    prepare_inventory_store()
    prepare_order_store()
    prepare_shipping_store()
    prepare_support_store()
    prepare_user_store()
    yield


app = FastAPI(title=settings.app_name, version="0.1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict[str, str]:
    return health_response()


app.include_router(api_router, prefix=settings.api_prefix)
