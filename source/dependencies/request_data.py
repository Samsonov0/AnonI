import re
from typing import Callable


class RequestData:
    def __init__(self, scope: dict, receive: Callable, path_regex: str, path: str):
        self._scope: dict = scope
        self._receive: Callable = receive
        self._path_regex: str = path_regex
        self._path: str = path

        self._path_parameters: dict = dict()
        self._query_parameters: dict = dict()

    async def __call__(self) -> "RequestData":
        await self._set_path_parameters()
        await self._set_query_parameters()

        return self

    async def _parse_url(self) -> dict[str:str] | None:
        match: dict[str:str] = re.match(self._path_regex, self._path)

        if match:
            return match.groupdict()
        return None

    async def _extract_query_string_data(self) -> dict[str:str]:
        query_string: bytes = self._scope.get("query_string")

        queries_list: list[str] = query_string.decode("utf-8").split("&")

        data: dict[str:str] = dict()

        for query in queries_list:
            equal_index: int = query.find("=")

            name: str = query[:equal_index:]
            value: str = query[equal_index + 1 : :]

            if name != "" and value != "":
                data[name] = value

        return data

    async def _extract_path_parameters(self) -> dict[str:str] | None:
        return await self._parse_url()

    async def _set_query_parameters(self) -> None:
        self._query_parameters = await self._extract_query_string_data()

    async def _set_path_parameters(self) -> None:
        self._path_parameters = await self._extract_path_parameters()

    def path_parameters(self) -> dict[str:str]:
        return self._path_parameters

    def query_parameters(self) -> dict[str:str]:
        return self._query_parameters

    def receive(self):
        return self._receive
