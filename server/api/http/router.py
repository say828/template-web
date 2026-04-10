from fastapi import APIRouter

from contexts.alerts.contracts.http.router import router as alerts_router
from contexts.auth.contracts.http.router import router as auth_router
from contexts.catalog.contracts.http.router import router as catalog_router
from contexts.fulfillment.contracts.http.router import router as fulfillment_router
from contexts.health.contracts.http.router import router as health_router
from contexts.inventory.contracts.http.router import router as inventory_router
from contexts.orders.contracts.http.router import router as orders_router
from contexts.shipping.contracts.http.router import router as shipping_router
from contexts.support.contracts.http.router import router as support_router
from contexts.user.contracts.http.router import router as user_router

api_router = APIRouter()
api_router.include_router(alerts_router)
api_router.include_router(auth_router)
api_router.include_router(catalog_router)
api_router.include_router(fulfillment_router)
api_router.include_router(health_router)
api_router.include_router(inventory_router)
api_router.include_router(orders_router)
api_router.include_router(shipping_router)
api_router.include_router(support_router)
api_router.include_router(user_router)
