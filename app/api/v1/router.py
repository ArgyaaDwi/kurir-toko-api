from fastapi import APIRouter

from app.api.v1.endpoints import batching, global_pricing, health, pricing, routing


api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(routing.router, prefix="/routes", tags=["routes"])
api_router.include_router(batching.router, prefix="/batches", tags=["batches"])
api_router.include_router(pricing.router, prefix="/pricing", tags=["pricing"])
api_router.include_router(global_pricing.router, prefix="/pricing", tags=["pricing"])
