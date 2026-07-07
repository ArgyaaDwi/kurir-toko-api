from fastapi import APIRouter, Body

from app.api.openapi_examples import BATCH_REQUEST_EXAMPLES, BATCH_RESPONSE_EXAMPLE
from app.schemas.batching import BatchPlanRequest, BatchPlanResponse
from app.services.batching_service import plan_batches


router = APIRouter()


@router.post(
    "/plan",
    response_model=BatchPlanResponse,
    summary="Rencanakan batch pengiriman",
    description="Membagi order ke beberapa batch berdasarkan cutoff time, lalu menghitung hasil routing per batch.",
    responses={
        200: {
            "description": "Batch pengiriman berhasil dibuat.",
            "content": {
                "application/json": {
                    "example": BATCH_RESPONSE_EXAMPLE,
                }
            },
        }
    },
)
def plan_batch(
    request: BatchPlanRequest = Body(..., openapi_examples=BATCH_REQUEST_EXAMPLES),
) -> BatchPlanResponse:
    return plan_batches(request)
