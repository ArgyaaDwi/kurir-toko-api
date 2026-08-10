from fastapi import APIRouter, Body

from app.api.openapi_examples import V2_OPTIMIZE_ROUTE_REQUEST_EXAMPLES, V2_OPTIMIZE_ROUTE_RESPONSE_EXAMPLE
from app.schemas.v2_routing import V2OptimizeRouteRequest, V2OptimizeRouteResponse
from app.services.v2_routing_service import optimize_v2_route


router = APIRouter()


@router.post(
    "/optimize",
    response_model=V2OptimizeRouteResponse,
    summary="Optimasi rute Laravel/Omni",
    description="Menerima payload route dari Laravel/Omni dan mengembalikan urutan pengiriman Kurir Toko Retail. Semua order dihitung sebagai MOBIL.",
    responses={
        200: {
            "description": "Rute berhasil dioptimasi.",
            "content": {
                "application/json": {
                    "example": V2_OPTIMIZE_ROUTE_RESPONSE_EXAMPLE,
                }
            },
        }
    },
)
def optimize_route(
    request: V2OptimizeRouteRequest = Body(..., openapi_examples=V2_OPTIMIZE_ROUTE_REQUEST_EXAMPLES),
) -> V2OptimizeRouteResponse:
    return optimize_v2_route(request)
