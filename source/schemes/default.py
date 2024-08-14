import json

from pydantic import BaseModel, Json, field_validator

from source.utils.status_code import HTTP_404_NOT_FOUND


class Headers(BaseModel):
    Authorization: str | None = None
    Content_Type: str | None = None
    Content_Length: str | None = None
    Host: str | None = None
    Accept: str | None = None
    Accept_Encoding: str | None = None
    Connection: str | None = None

    @field_validator("Authorization")
    @classmethod
    def set_authorization(cls, value: str | None) -> str:
        if value is None:
            return "none"
        return value

    @field_validator("Content_Type")
    @classmethod
    def set_content_type(cls, value: str | None) -> str:
        if value is None:
            return "application/json"
        return value

    @field_validator("Content_Length")
    @classmethod
    def set_content_length(cls, value: str | None) -> str:
        if value is None:
            return "none"
        return value

    @field_validator("Host")
    @classmethod
    def set_host(cls, value: str | None) -> str:
        if value is None:
            return "none"
        return value

    @field_validator("Accept")
    @classmethod
    def set_accept(cls, value: str | None) -> str:
        if value is None:
            return "none"
        return value

    @field_validator("Accept_Encoding")
    @classmethod
    def set_accept_encoding(cls, value: str | None) -> str:
        if value is None:
            return "none"
        return value

    @field_validator("Connection")
    @classmethod
    def set_connection(cls, value: str | None) -> str:
        if value is None:
            return "none"
        return value

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
