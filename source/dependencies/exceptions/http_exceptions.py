import json

from source.utils.status_code import HTTP_403_FORBIDDEN, HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST


class HTTPException(Exception):
    def __init__(self, status: int, message_type: str, message: str) -> None:
        self.status = status
        self.message_type = message_type
        self.message = message

    def get_exception(self) -> bytes:
        exception = json.dumps({self.message_type: self.message})

        return exception.encode("utf-8")


class HTTPForbidden(HTTPException):
    def __init__(
        self, message_type: str = "message", message: str = "Access not allowed"
    ) -> None:
        super().__init__(
            status=HTTP_403_FORBIDDEN, message_type=message_type, message=message
        )


class HTTPSuccess(HTTPException):
    def __init__(
        self, message_type: str = "message", message: str = "Success"
    ) -> None:
        super().__init__(
            status=HTTP_200_OK, message_type=message_type, message=message
        )


class HTTPNotFound(HTTPException):
    def __init__(
        self, message_type: str = "message", message: str = "Not Found"
    ) -> None:
        super().__init__(
            status=HTTP_404_NOT_FOUND, message_type=message_type, message=message
        )


class HTTPBadRequest(HTTPException):
    def __init__(
        self, message_type: str = "message", message: str = "Bad Request"
    ) -> None:
        super().__init__(
            status=HTTP_400_BAD_REQUEST, message_type=message_type, message=message
        )


