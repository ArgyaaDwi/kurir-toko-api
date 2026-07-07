from fastapi import APIRouter, Body

from app.api.openapi_examples import GLOBAL_PRICING_REQUEST_EXAMPLES, GLOBAL_PRICING_RESPONSE_EXAMPLE
from app.schemas.global_pricing import GlobalDeliveryCostRequest, GlobalDeliveryCostResponse
from app.services.global_pricing_service import calculate_global_delivery_cost


router = APIRouter()


@router.post(
    "/global-estimate",
    response_model=GlobalDeliveryCostResponse,
    summary="Hitung ongkir global",
    description="Menghitung ongkir dengan variabel biaya global tanpa perlu mengirim vehicle type dari client.",
    responses={
        200: {
            "description": "Ongkir global berhasil dihitung.",
            "content": {
                "application/json": {
                    "example": GLOBAL_PRICING_RESPONSE_EXAMPLE,
                }
            },
        }
    },
)
def estimate_global_delivery_cost(
    request: GlobalDeliveryCostRequest = Body(..., openapi_examples=GLOBAL_PRICING_REQUEST_EXAMPLES),
) -> GlobalDeliveryCostResponse:
    return calculate_global_delivery_cost(request)
