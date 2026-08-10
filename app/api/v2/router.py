from fastapi import APIRouter

from app.api.v2.endpoints import routes


api_router = APIRouter()
api_router.include_router(routes.router, prefix="/routes", tags=["v2-routes"])
