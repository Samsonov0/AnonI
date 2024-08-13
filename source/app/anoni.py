import json
import re

import uvicorn

from source.dependencies import RequestData
from source.schemes.default import NotFound404
from source.utils.fill_scheme import fill_scheme


class Anoni:
    def __init__(self, app_name, host, port, log_level):
        self.app_name = app_name
        self.host = host
        self.port = port
        self.log_level = log_level

        self.url_paths = dict()

    async def __call__(self, scope, receive, send):
        if scope['type'] == 'http':
            called = False

            path: str = scope['path'].strip()
            method: str = scope['method']

            for path_data, handler in self.url_paths.items():

                path_regex, excepted_method = path_data

                match = self._path_matched_with_path_regex(path_regex, path)

                if match and method == excepted_method:
                    request_data = RequestData(scope=scope, receive=receive, path_regex=path_regex, path=path)()

                    if method == 'GET':
                        handler_response = await handler(request_data=request_data)
                    elif method in ('POST', 'PUT', 'PATCH'):
                        body = await self._get_body(receive)
                        filled_scheme = await fill_scheme(handler, body)
                        handler_response = await handler(scheme=filled_scheme, request_data=request_data)
                    elif method == 'DELETE':
                        handler_response = await handler(request_data=request_data)

                    await self.send_response(send, handler_response)

                    called = True
                    break

            if not called:
                page_not_fund = NotFound404()
                await self.send_response(send, page_not_fund)

    def _parse_url(self, pattern: str, string: str):
        match = re.match(pattern, string)

        if match:
            return match.groupdict()
        return None

    def _path_matched_with_path_regex(self, path_regex, path):
        return re.match(path_regex, path) is not None

    async def _get_body(self, receive) -> dict:
        body = b''
        while True:
            message = await receive()
            if message['type'] == 'http.request':
                body += message.get('body', b'')
                if not message.get('more_body', False):
                    break

        body_str = body.decode('utf-8')

        body_data = json.loads(body_str)

        return body_data

    async def send_response(self, send, response_scheme):
        status = response_scheme.status
        headers = response_scheme.headers
        body = response_scheme.body_to_json()

        if body is None:
            body = ''

        await send({
            "type": "http.response.start",
            "status": status,
            "headers": headers.to_tuple_list()
        })

        await send({
            "type": "http.response.body",
            "body": body.encode('utf-8'),
        })

    def start_app(self):
        uvicorn.run(self) #  Пробросить порт хост и лог_левел

    def register_router(self, router):
        self.url_paths.update(
            {key: value for key, value in router._paths.items() if key not in self.url_paths}
        )

#  Сделать возможность получать параметры строки: http://127.0.1:8000/api/users/?name=Joe&age=18&data={"data": True}
