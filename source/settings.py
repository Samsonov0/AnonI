import importlib.util
import os
import sys

from source.schemes.default import Headers


class Settings:
    _default_field = {
        "JWT_SECRET": "DEFAULT",  # (!) PLEASE SET YOUR OWN JWT_SECRET IN YOUR SETTINGS
        "JWT_ALGORITHM": "HS256",
        "HEADERS": Headers(),
        "CURRENT_DIRECTORY": os.getcwd(),
        "JWT_LIVE_TIME_SEC": 1800,
        "JWT_REFRESH_LIVE_TIME_SEC": 10800,
    }

    def __init__(self, settings_path: str | None = "settings.py"):
        self._defaults = self._default_field
        self._user_settings = self._check_get_settings(settings_path)

    def __call__(self, *args, **kwargs):
        return self

    def __getattr__(self, name):
        if self._user_settings and hasattr(self._user_settings, name):
            return getattr(self._user_settings, name)
        elif name in self._defaults:
            return self._defaults[name]
        raise AttributeError(f"Setting '{name}' not found.")

    def _load_settings_from_file(self, settings_path):
        spec = importlib.util.spec_from_file_location("settings", settings_path)
        user_settings = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(user_settings)
        return user_settings

    def _check_get_settings(self, settings_path: str):
        print(f"\033[31mProject settings checking\033[0m")
        if not os.path.isfile(settings_path):
            print(f"\033[31mSettings file not found: {settings_path}\033[0m")
            sys.exit(1)
        else:
            print("\033[32mSettings are set\033[0m")

        project_settings = self._load_settings_from_file(settings_path)

        return project_settings


def get_settings(path_to_settings: str = "settings.py"):
    return globals().get("settings", Settings(settings_path=path_to_settings)())


SETTINGS = get_settings()
