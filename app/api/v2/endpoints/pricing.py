from fastapi import APIRouter, Body

from app.api.openapi_examples import (
    V2_GLOBAL_PRICING_REQUEST_EXAMPLES,
    V2_GLOBAL_PRICING_RESPONSE_EXAMPLE,
)
from app.schemas.v2_pricing import V2GlobalDeliveryCostRequest, V2GlobalDeliveryCostResponse
from app.services.v2_pricing_service import calculate_v2_global_delivery_cost


router = APIRouter()


@router.post(
    "/global-estimate",
    response_model=V2GlobalDeliveryCostResponse,
    summary="Hitung ongkir global berdasarkan isi invoice",
    description=(
        "Menentukan MOTOR atau MOBIL dari SKU, dimensi, dan total berat invoice; "
        "lalu menghitung ongkir dengan tarif kendaraan yang terpilih."
    ),
    responses={
        200: {
            "description": "Kendaraan dan ongkir berhasil dihitung.",
            "content": {
                "application/json": {
                    "example": V2_GLOBAL_PRICING_RESPONSE_EXAMPLE,
                }
            },
        }
    },
)
def estimate_v2_global_delivery_cost(
    request: V2GlobalDeliveryCostRequest = Body(
        ..., openapi_examples=V2_GLOBAL_PRICING_REQUEST_EXAMPLES
    ),
) -> V2GlobalDeliveryCostResponse:
    return calculate_v2_global_delivery_cost(request)
