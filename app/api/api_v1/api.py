from fastapi import APIRouter

from app.api.api_v1.endpoints import courier, order

api_router = APIRouter()
api_router.include_router(order.router, prefix="/orders", tags=["order-controller"])
api_router.include_router(
    courier.router, prefix="/couriers", tags=["courier-controller"]
)
