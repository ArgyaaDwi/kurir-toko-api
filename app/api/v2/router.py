from fastapi import APIRouter

from app.api.v2.endpoints import retail_orders


api_router = APIRouter()
api_router.include_router(retail_orders.router, prefix="/retail", tags=["v2-retail"])
