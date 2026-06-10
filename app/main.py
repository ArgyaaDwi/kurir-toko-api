from fastapi import FastAPI

from app.api.v1.router import api_router


app = FastAPI(
    title="Kurir Toko API",
    version="0.1.0",
    description="POC API for Kurir Toko routing and batch planning.",
)

app.include_router(api_router, prefix="/api/v1")


@app.get("/", tags=["root"])
def root() -> dict:
    return {
        "service": "kurir-toko-api",
        "version": "0.1.0",
        "docs": "/docs",
    }

