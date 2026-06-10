from fastapi import APIRouter

from app.schemas.routing import OptimizeRouteRequest, OptimizeRouteResponse
from app.services.routing_service import optimize_routes


router = APIRouter()


@router.post("/optimize", response_model=OptimizeRouteResponse)
def optimize_route(request: OptimizeRouteRequest) -> OptimizeRouteResponse:
    return optimize_routes(request)

