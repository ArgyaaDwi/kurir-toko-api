from fastapi import APIRouter

from app.schemas.batching import BatchPlanRequest, BatchPlanResponse
from app.services.batching_service import plan_batches


router = APIRouter()


@router.post("/plan", response_model=BatchPlanResponse)
def plan_batch(request: BatchPlanRequest) -> BatchPlanResponse:
    return plan_batches(request)

