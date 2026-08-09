from fastapi import APIRouter, Body

from app.api.openapi_examples import RETAIL_ORDER_ESTIMATE_REQUEST_EXAMPLES, RETAIL_ORDER_ESTIMATE_RESPONSE_EXAMPLE
from app.schemas.retail_order import RetailOrderEstimateRequest, RetailOrderEstimateResponse
from app.services.retail_order_service import estimate_retail_order_shipping


router = APIRouter()


@router.post(
    "/orders/shipping-estimate",
    response_model=RetailOrderEstimateResponse,
    summary="Hitung ongkir order retail Omni",
    description="Menerima payload order real dari Omni dan menghitung ongkir Kurir Toko Retail dari warehouse ke alamat customer.",
    responses={
        200: {
            "description": "Estimasi ongkir Kurir Toko Retail berhasil dihitung.",
            "content": {
                "application/json": {
                    "example": RETAIL_ORDER_ESTIMATE_RESPONSE_EXAMPLE,
                }
            },
        }
    },
)
def estimate_shipping(
    request: RetailOrderEstimateRequest = Body(..., openapi_examples=RETAIL_ORDER_ESTIMATE_REQUEST_EXAMPLES),
) -> RetailOrderEstimateResponse:
    return estimate_retail_order_shipping(request)
