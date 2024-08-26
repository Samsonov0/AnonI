import json
import re
from typing import Callable, Optional, Type

import uvicorn
from pydantic import BaseModel

from source.arg_parser.example_project.settings import HEADERS
from source.dependencies import RequestData, ResponseData
from source.dependencies.exceptions import HTTPException
from source.dependencies.middlewares.default import AbstractMiddleware
from source.routers import DefaultRouter
from source.schemes.default import Headers, NotFound404
from source.schemes.extra import ExtraPathSettings
from source.utils import HTTP_DELETE, HTTP_GET, HTTP_PATCH, HTTP_POST, HTTP_PUT
from source.utils.fill_scheme import fill_scheme


class Anoni:
    def __init__(self, app_name: str, host: str, port: str, log_level: str):
        self.app_name: str = app_name
        self.host: str = host
        self.port: str = port
        self.log_level: str = log_level

        self.url_paths: dict[tuple[str:str]: Callable] = dict()
        self.before_middleware: list[Type[AbstractMiddleware]] = []
        self.after_middleware: list[Type[AbstractMiddleware]] = []

    async def __call__(self, scope: dict, receive: Callable, send: Callable):
        if scope["type"] == "http":
            called: bool = False

            path: str = scope["path"].strip()
            method: str = scope["method"]

            for path_data, handler in self.url_paths.items():
                path_regex, excepted_method, extra = path_data

                match: bool = re.match(path_regex, path) is not None

                try:
                    if match and method == excepted_method:
                        request_data: RequestData = await RequestData(
                            scope=scope,
                            receive=receive,
                            path_regex=path_regex,
                            path=path,
                        )()

                        response_data = await self._process_response(
                            request_data=request_data,
                            method=method,
                            handler=handler,
                            extra=extra,
                        )

                        await self._send_response(send, response_data)

                        called = True
                        break

                except HTTPException as e:
                    await self._send_exception(send=send, exception=e)

                    called = True
                    break

            if not called:
                page_not_fund = NotFound404()

                response_data = ResponseData(scheme=page_not_fund)

                await self._send_response(send, response_data)

    async def _process_response(
        self,
        request_data: RequestData,
        method: str,
        handler: Callable,
        extra: Optional[ExtraPathSettings] = None,
    ) -> ResponseData:
        request_data = await self._process_before_middlewares(
            request_data=request_data, extra=extra
        )
        response_data = await self._call_handler(
            request_data=request_data, method=method, handler=handler
        )
        response_data = await self._process_after_middlewares(
            response_data=response_data, extra=extra
        )
        return response_data

    async def _send_exception(self, send: Callable, exception: HTTPException) -> None:
        await self._send_server_response(
            send=send,
            status=exception.status,
            headers=HEADERS.to_tuple_list(),
            body=exception.get_exception(),
        )

    async def _send_response(self, send: Callable, response_data: ResponseData) -> None:
        response = response_data.response()

        status: int = response.status
        headers: Headers = response.headers
        body: str = response.body_to_json()

        if body is None:
            body: str = ""

        await self._send_server_response(
            send=send,
            status=status,
            headers=headers.to_tuple_list(),
            body=body.encode("utf-8"),
        )

    def start_app(self) -> None:
        uvicorn.run(self)  # Пробросить порт хост и лог_левел

    async def _call_handler(
        self,
        request_data: RequestData,
        method: str,
        handler: Callable,
    ) -> ResponseData:
        if method in (HTTP_GET, HTTP_DELETE):
            response_data: ResponseData = await handler(request_data=request_data)
        elif method in (HTTP_POST, HTTP_PUT, HTTP_PATCH):
            body: dict = await self._get_body(request_data.receive())
            filled_scheme: BaseModel = await fill_scheme(handler, body)
            response_data: ResponseData = await handler(
                scheme=filled_scheme, request_data=request_data
            )

        return response_data

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

    async def _send_server_response(
        self, send: Callable, status: int, headers: list, body: bytes
    ) -> None:
        await send(
            {
                "type": "http.response.start",
                "status": status,
                "headers": headers,
            }
        )

        await send(
            {
                "type": "http.response.body",
                "body": body,
            }
        )

    async def register_router(
        self, router: DefaultRouter | tuple[DefaultRouter, ...]
    ) -> None:
        for count in range(len(router)):
            self.url_paths.update(
                {
                    key: value
                    for key, value in router.paths().items()
                    if key not in self.url_paths
                }
            )

    async def register_middleware(self, call: str, middleware) -> None:
        call: str = call.lower()

        if call not in ("before", "after"):
            raise ValueError("Call parameter have to be 'after' or 'before' only")
        # elif issubclass(middleware, AbstractMiddleware):
        #     raise ValueError(
        #         "Middleware parameter have to be child of AbstractMiddleware"
        #     )

        if call == "before":
            self.before_middleware.append(middleware)
        elif call == "after":
            self.after_middleware.append(middleware)

    async def _process_before_middlewares(
        self, request_data: RequestData, extra: Optional[ExtraPathSettings] = None
    ) -> RequestData:
        exclude_middlewares = ()

        if extra is not None:
            exclude_middlewares = extra.exclude_middlewares

        if "__all__" not in exclude_middlewares:
            for middleware in self.before_middleware:
                if middleware.__name__ not in exclude_middlewares:
                    middleware_instance = middleware(
                        request_data=request_data,
                    )
                    request_data = await middleware_instance()

        return request_data

    async def _process_after_middlewares(
        self, response_data: ResponseData, extra: Optional[ExtraPathSettings] = None
    ) -> ResponseData:
        exclude_middlewares = ()

        if extra is not None:
            exclude_middlewares = extra.exclude_middlewares

        if "__all__" not in exclude_middlewares:
            for middleware in self.after_middleware:
                if middleware.__name__ not in exclude_middlewares:
                    middleware_instance = middleware(
                        response_data=response_data,
                    )
                    response_data = await middleware_instance()

        return response_data
