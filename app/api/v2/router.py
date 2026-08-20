from fastapi import APIRouter

from app.api.v2.endpoints import pricing, routes


api_router = APIRouter()
api_router.include_router(routes.router, prefix="/routes", tags=["v2-routes"])
api_router.include_router(pricing.router, prefix="/pricing", tags=["v2-pricing"])
