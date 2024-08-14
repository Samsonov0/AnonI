import json
import re
from typing import Callable

import uvicorn
from pydantic import BaseModel

from source.dependencies import RequestData
from source.routers import DefaultRouter
from source.schemes import DefaultScheme
from source.schemes.default import Headers, NotFound404
from source.utils.fill_scheme import fill_scheme


class Anoni:
    def __init__(self, app_name: str, host: str, port: str, log_level: str):
        self.app_name: str = app_name
        self.host: str = host
        self.port: str = port
        self.log_level: str = log_level

        self.url_paths: dict[tuple[str:str] : Callable] = dict()

    async def __call__(self, scope: dict, receive: Callable, send: Callable):
        if scope["type"] == "http":
            called: bool = False

            path: str = scope["path"].strip()
            method: str = scope["method"]

            for path_data, handler in self.url_paths.items():

                path_regex, excepted_method = path_data

                match: bool = await self._path_matched_with_path_regex(path_regex, path)

                if match and method == excepted_method:
                    request_data: RequestData = await RequestData(
                        scope=scope, receive=receive, path_regex=path_regex, path=path
                    )()

                    if method in ("GET", "DELETE"):
                        handler_response: DefaultScheme = await handler(
                            request_data=request_data
                        )
                    elif method in ("POST", "PUT", "PATCH"):
                        body: dict = await self._get_body(receive)
                        filled_scheme: BaseModel = await fill_scheme(handler, body)
                        handler_response: DefaultScheme = await handler(
                            scheme=filled_scheme, request_data=request_data
                        )

                    await self.send_response(send, handler_response)

                    called: bool = True
                    break

            if not called:
                page_not_fund = NotFound404()
                await self.send_response(send, page_not_fund)

    async def _path_matched_with_path_regex(self, path_regex: str, path: str) -> bool:
        return re.match(path_regex, path) is not None

    async def _get_body(self, receive) -> dict:
        body: bytes = b""
        while True:
            message: dict = await receive()
            if message["type"] == "http.request":
                body += message.get("body", b"")
                if not message.get("more_body", False):
                    break

        body_str: str = body.decode("utf-8")

        body_data: dict = json.loads(body_str)

        return body_data

    async def send_response(
        self, send: Callable, response_scheme: DefaultScheme
    ) -> None:
        status: int = response_scheme.status
        headers: Headers = response_scheme.headers
        body: str = response_scheme.body_to_json()

        if body is None:
            body: str = ""

        await send(
            {
                "type": "http.response.start",
                "status": status,
                "headers": headers.to_tuple_list(),
            }
        )

        await send(
            {
                "type": "http.response.body",
                "body": body.encode("utf-8"),
            }
        )

    def start_app(self) -> None:
        uvicorn.run(self)  # Пробросить порт хост и лог_левел

    async def register_router(self, router: DefaultRouter) -> None:
        self.url_paths.update(
            {
                key: value
                for key, value in router.paths().items()
                if key not in self.url_paths
            }
        )
