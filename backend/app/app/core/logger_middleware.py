import json
import random
import string
import time

from loguru import logger
from starlette.datastructures import URL
from starlette.responses import RedirectResponse
from starlette.types import ASGIApp, Receive, Scope, Send


class LoggerMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        idem = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        server_host_port = scope.get("server")
        client_host_port = scope.get("client")
        http_method = scope.get("method")
        url_path = scope.get("path")
        logger.info(f"rid={idem} start request server={server_host_port}, client={client_host_port}, api={http_method} {url_path}")
        start_time = time.time()

        await self.app(scope, receive, send)

        process_time = (time.time() - start_time) * 1000
        formatted_process_time = '{0:.2f}'.format(process_time)
        logger.info(f"rid={idem} completed_in={formatted_process_time}ms status_code=XXX")