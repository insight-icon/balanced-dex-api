from fastapi import APIRouter

from app.api.api_v1.endpoints import dex, eventer, crud, balanced, depth, kline, address

api_router = APIRouter()
api_router.include_router(dex.router, prefix="/dex",   tags=["dex"])
api_router.include_router(eventer.router, prefix="/eventer",   tags=["eventer"])
api_router.include_router(crud.router, prefix="/crud", tags=["crud"])

api_router.include_router(balanced.router, prefix="/balanced", tags=["balanced"])
api_router.include_router(depth.router, prefix="/balanced/depth", tags=["depth"])
api_router.include_router(kline.router, prefix="/balanced/kline", tags=["kline"])
api_router.include_router(address.router, prefix="/balanced/address", tags=["address"])
