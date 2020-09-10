import random
import string
import time

from starlette.datastructures import URL
from loguru import logger
from starlette.types import ASGIApp, Receive, Scope, Send


class SecondMiddleware:
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
        logger.info(f"rid={idem} completed_in={formatted_process_time}ms status_code=YYY")
