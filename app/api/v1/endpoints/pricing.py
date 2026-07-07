from fastapi import APIRouter, Body

from app.api.openapi_examples import PRICING_REQUEST_EXAMPLES, PRICING_RESPONSE_EXAMPLE
from app.schemas.pricing import DeliveryCostRequest, DeliveryCostResponse
from app.services.pricing_service import calculate_delivery_cost


router = APIRouter()


@router.post(
    "/estimate",
    response_model=DeliveryCostResponse,
    summary="Hitung ongkir per kendaraan",
    description="Menghitung jarak, durasi, dan ongkir dari koordinat asal ke tujuan berdasarkan vehicle type yang dikirim.",
    responses={
        200: {
            "description": "Ongkir berhasil dihitung.",
            "content": {
                "application/json": {
                    "example": PRICING_RESPONSE_EXAMPLE,
                }
            },
        }
    },
)
def estimate_delivery_cost(
    request: DeliveryCostRequest = Body(..., openapi_examples=PRICING_REQUEST_EXAMPLES),
) -> DeliveryCostResponse:
    return calculate_delivery_cost(request)
