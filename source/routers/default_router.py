import re
from typing import Callable, Optional

from source.schemes.extra import ExtraPathSettings


class DefaultRouter:
    def __init__(
        self,
        name: str,
        description: str,
        prefix: str = "",
        extra: ExtraPathSettings | None = None,
    ):
        self._name: str = name
        self._description: str = description
        self._paths: dict[tuple[str, str] : Callable] = dict()
        self._prefix: str = prefix
        self._extra = extra

    def __len__(self):
        return 1

    def _path_to_regex(self, path: str) -> str:
        path_regex: str = re.sub(r"{(\w+)}", r"(?P<\1>[^/]+)", path)
        path_regex: str = f"^{path_regex}$"

        return path_regex

    def _modernize_path(self, path: str) -> str:
        if not path.startswith("/"):
            path = "/" + path

        path_with_prefix: str = self._prefix + path

        return self._path_to_regex(path_with_prefix)

    def paths(self) -> dict[tuple[str, str] : Callable]:
        return self._paths

    def get(self, path: str, extra: Optional[ExtraPathSettings] = None) -> Callable:
        def wrapper(func: Callable, *args, **kwargs) -> None:
            extra_settings = self._extra if extra is None else extra

            correct_path: str = self._modernize_path(path)

            key: tuple[str, str, ExtraPathSettings] = (
                correct_path,
                "GET",
                extra_settings,
            )

            self._paths[key] = func

        return wrapper

    def post(self, path: str, extra: Optional[ExtraPathSettings] = None) -> Callable:
        def wrapper(func, *args, **kwargs) -> None:
            extra_settings = self._extra if extra is None else extra

            correct_path: str = self._modernize_path(path)

            key: tuple[str, str, ExtraPathSettings] = (
                correct_path,
                "POST",
                extra_settings,
            )

            self._paths[key] = func

        return wrapper

    def put(self, path: str, extra: Optional[ExtraPathSettings] = None) -> Callable:
        def wrapper(func, *args, **kwargs) -> None:
            extra_settings = self._extra if extra is None else extra

            correct_path: str = self._modernize_path(path)

            key: tuple[str, str, ExtraPathSettings] = (
                correct_path,
                "PUT",
                extra_settings,
            )

            self._paths[key] = func

        return wrapper

    def patch(self, path: str, extra: Optional[ExtraPathSettings] = None) -> Callable:
        def wrapper(func, *args, **kwargs) -> None:
            extra_settings = self._extra if extra is None else extra

            correct_path: str = self._modernize_path(path)

            key: tuple[str, str, ExtraPathSettings] = (
                correct_path,
                "PATCH",
                extra_settings,
            )

            self._paths[key] = func

        return wrapper

    def delete(self, path: str, extra: Optional[ExtraPathSettings] = None) -> Callable:
        def wrapper(func, *args, **kwargs) -> None:
            extra_settings = self._extra if extra is None else extra

            correct_path: str = self._modernize_path(path)

            key: tuple[str, str, ExtraPathSettings] = (
                correct_path,
                "DELETE",
                extra_settings,
            )

            self._paths[key] = func

        return wrapper
