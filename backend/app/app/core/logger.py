# from starlette.middleware.base import BaseHTTPMiddleware
# import random
# import string
# import time
# from loguru import logger
# # from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware

# class Logger(BaseHTTPMiddleware):
#     async def dispatch(self, request, call_next):
#         idem = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
#         logger.info(f"rid={idem} start request path={request.url.path}")
#         start_time = time.time()
#
#         response = await call_next(request)
#         # response.headers['Custom'] = 'Example'
#         # return response
#
#
#         process_time = (time.time() - start_time) * 1000
#         formatted_process_time = '{0:.2f}'.format(process_time)
#         logger.info(f"rid={idem} completed_in={formatted_process_time}ms status_code={response.status_code}")
#
#         return response
###########################

import random
import string
import time

from starlette.datastructures import URL
from loguru import logger
from starlette.types import ASGIApp, Receive, Scope, Send


class Logger:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        idem = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        url = URL(scope=scope)
        logger.info(f"rid={idem} start request path={url.path}")
        start_time = time.time()

        await self.app(scope, receive, send)

        process_time = (time.time() - start_time) * 1000
        formatted_process_time = '{0:.2f}'.format(process_time)
        logger.info(f"rid={idem} completed_in={formatted_process_time}ms status_code=XXX")


################
# from fastapi.requests import Request
# from loguru import logger
# import random
# import string
# import time
#
# from app import app
#
#
# @app.middleware("http")
# async def log_requests(request: Request, call_next):
#     idem = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
#     logger.info(f"rid={idem} start request path={request.url.path}")
#     start_time = time.time()
#
#     response = await call_next(request)
#
#     process_time = (time.time() - start_time) * 1000
#     formatted_process_time = '{0:.2f}'.format(process_time)
#     logger.info(f"rid={idem} completed_in={formatted_process_time}ms status_code={response.status_code}")
#
#     return response
