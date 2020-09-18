from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.api_v1.api import api_router
from app.core.config import settings
from app.core.logger_middleware import LoggerMiddleware

from app.core.logger_config import LoggerConfig
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

LoggerConfig()  # configures loguru logger

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


# todo: introduces =>   INFO:     ASGI 'lifespan' protocol appears unsupported.
# todo: which in turn is causing test fixture for getting client to fail
app.add_middleware(LoggerMiddleware)


app.include_router(api_router, prefix=settings.API_V1_STR)
