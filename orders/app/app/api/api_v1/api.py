from fastapi import APIRouter

from app.api.api_v1.endpoints import balanced, depth, kline, transaction

api_router = APIRouter()

api_router.include_router(balanced.router, prefix="/balanced", tags=["balanced"])
api_router.include_router(depth.router, prefix="/balanced/depth", tags=["depth"])
api_router.include_router(kline.router, prefix="/balanced/kline", tags=["kline"])
api_router.include_router(transaction.router, prefix="/balanced/transaction", tags=["transaction"])
