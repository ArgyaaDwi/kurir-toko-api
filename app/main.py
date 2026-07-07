from fastapi import FastAPI

from app.api.v1.router import api_router
from app.api.openapi_examples import ROOT_RESPONSE_EXAMPLE


openapi_tags = [
    {"name": "root", "description": "Informasi dasar service dan link dokumentasi."},
    {"name": "health", "description": "Endpoint sederhana untuk health check service."},
    {"name": "routes", "description": "Optimasi urutan pengantaran untuk banyak order."},
    {"name": "batches", "description": "Pembagian order ke batch berdasarkan cutoff time."},
    {"name": "pricing", "description": "Perhitungan ongkir dari koordinat asal ke tujuan."},
]


app = FastAPI(
    title="Kurir Toko API",
    version="0.1.0",
    description="POC API untuk routing, batching, dan perhitungan ongkir Kurir Toko.",
    openapi_tags=openapi_tags,
)

app.include_router(api_router, prefix="/api/v1")


@app.get(
    "/",
    tags=["root"],
    summary="Info service",
    description="Mengembalikan identitas service dan path dokumentasi Swagger.",
    responses={
        200: {
            "description": "Informasi service berhasil diambil.",
            "content": {
                "application/json": {
                    "example": ROOT_RESPONSE_EXAMPLE,
                }
            },
        }
    },
)
def root() -> dict:
    return {
        "service": "kurir-toko-api",
        "version": "0.1.0",
        "docs": "/docs",
    }
