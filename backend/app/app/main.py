from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.api_v1.api import api_router
from app.core.config import settings
from app.core.logger_middleware import LoggerMiddleware
from app.core.second_middleware import SecondMiddleware

from app.core.logger_config import LoggerConfig

# from elasticapm.contrib.starlette import make_apm_client, ElasticAPM
#
#
# elasticapm = make_apm_client({
#     'SERVICE_NAME': 'dex-api-main',
#     'SECRET_TOKEN': 'secret-token-apm-client',
#     'SERVER_URL': 'http://localhost:5000'
# })
# #============

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

# app.add_middleware(ElasticAPM, client=elasticapm)
app.add_middleware(LoggerMiddleware)  # todo: introduces =>   INFO:     ASGI 'lifespan' protocol appears unsupported.
# app.add_middleware(SecondMiddleware)

app.include_router(api_router, prefix=settings.API_V1_STR)
