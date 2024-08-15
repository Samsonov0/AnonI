from source.schemes import DefaultScheme


class ResponseData:
    def __init__(self, scheme: DefaultScheme) -> None:
        self._response: DefaultScheme = scheme

    async def _validate_response(self, response: DefaultScheme) -> bool:
        if not isinstance(response, DefaultScheme):
            return False
        return True

    async def _set_response(self, response: DefaultScheme) -> None:
        is_valid = await self._validate_response(response)
        if is_valid:
            self._response = response

    def response(self) -> DefaultScheme:
        return self._response
