from fastapi import APIRouter

from app.api.openapi_examples import HEALTH_RESPONSE_EXAMPLE


router = APIRouter()


@router.get(
    "/health",
    summary="Health check",
    description="Mengecek apakah service aktif dan bisa menerima request.",
    responses={
        200: {
            "description": "Service dalam kondisi sehat.",
            "content": {
                "application/json": {
                    "example": HEALTH_RESPONSE_EXAMPLE,
                }
            },
        }
    },
)
def health() -> dict:
    return {"status": "ok"}
