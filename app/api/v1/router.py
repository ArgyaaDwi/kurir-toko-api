from fastapi import APIRouter

from app.api.v1.endpoints import batching, health, routing


api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(routing.router, prefix="/routes", tags=["routes"])
api_router.include_router(batching.router, prefix="/batches", tags=["batches"])

