from fastapi import APIRouter, Body

from app.api.openapi_examples import ROUTING_REQUEST_EXAMPLES, ROUTING_RESPONSE_EXAMPLE
from app.schemas.routing import OptimizeRouteRequest, OptimizeRouteResponse
from app.services.routing_service import optimize_routes


router = APIRouter()


@router.post(
    "/optimize",
    response_model=OptimizeRouteResponse,
    summary="Optimasi rute order",
    description="Mengurutkan pengiriman order berdasarkan cabang, hasil geocoding, dan algoritma optimasi yang dipilih.",
    responses={
        200: {
            "description": "Rute berhasil dioptimasi.",
            "content": {
                "application/json": {
                    "example": ROUTING_RESPONSE_EXAMPLE,
                }
            },
        }
    },
)
def optimize_route(
    request: OptimizeRouteRequest = Body(..., openapi_examples=ROUTING_REQUEST_EXAMPLES),
) -> OptimizeRouteResponse:
    return optimize_routes(request)
