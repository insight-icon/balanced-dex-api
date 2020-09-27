from fastapi import APIRouter

from app.api.api_v1.endpoints import dex, eventer, crud

api_router = APIRouter()
api_router.include_router(dex.router, prefix="/dex",   tags=["dex"])
api_router.include_router(eventer.router, prefix="/eventer",   tags=["eventer"])
api_router.include_router(crud.router, prefix="/crud", tags=["crud"])
api_router.include_router(crud.router, prefix="/balanced", tags=["balanced"])
