from source.dependencies import RequestData
from source.dependencies.response_data import ResponseData


class AbstractMiddleware:
    def __init__(self, request_data: RequestData | None = None, response_data: ResponseData | None = None) -> None:
        self.request_data: RequestData = request_data
        self.response_data: ResponseData = response_data

    async def __call__(self):
        return await self._processing()

    async def _processing(self):
        ...


class BeforeMiddleware(AbstractMiddleware):
    async def _processing(self):
        print(self.request_data, 'request')

        return self.request_data


class AfterMiddleware(AbstractMiddleware):
    async def _processing(self):
        print(self.response_data, 'response')

        return self.response_data