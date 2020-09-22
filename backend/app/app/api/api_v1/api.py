from fastapi import APIRouter

from app.api.api_v1.endpoints import dex, eventer

api_router = APIRouter()
api_router.include_router(dex.router,   prefix="/dex",   tags=["dex"])
api_router.include_router(eventer.router,   prefix="/eventer",   tags=["eventer"])
