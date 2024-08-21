import json

from pydantic import BaseModel, Json

from source.utils.status_code import HTTP_404_NOT_FOUND


class Headers(BaseModel):
    authorization: str | None = None
    content_type: str | None = "application/json"
    content_length: str | None = None
    host: str | None = None
    accept: str | None = None
    accept_encoding: str | None = None
    connection: str | None = None
    user_agent: str | None = None

    def to_tuple_list(self) -> list[tuple[bytes, bytes]]:
        return [
            (key.encode("utf-8"), value.encode("utf-8"))
            for key, value in self.dict().items()
            if value is not None
        ]


class DefaultScheme(BaseModel):
    status: int
    headers: Headers = Headers()
    body: Json | dict | None = None

    def body_to_json(self) -> str | None:
        body = self.dict().get("body")

        if body is not None and isinstance(body, dict):
            body = json.dumps(body)
        return body


class NotFound404(DefaultScheme):
    status: int = HTTP_404_NOT_FOUND
    body: Json = json.dumps({"message": "Page not found"})
