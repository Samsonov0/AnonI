import re


class DefaultRouter:
    def __init__(self, name: str, description: str, prefix: str = ''):
        self._name = name
        self._description = description
        self._paths = dict()
        self._prefix = prefix

    def _path_to_regex(self, path):
        path_regex = re.sub(r'{(\w+)}', r'(?P<\1>[^/]+)', path)
        path_regex = f'^{path_regex}$'

        return path_regex

    def _modernize_path(self, path: str):
        if not path.startswith('/'):
            path = '/' + path

        path_with_prefix = self._prefix + path

        return self._path_to_regex(path_with_prefix)

    def get(self, path: str):
        def wrapper(func, *args, **kwargs):
            correct_path = self._modernize_path(path)

            key = (correct_path, 'GET')

            self._paths[key] = func

        return wrapper

    def post(self, path: str):
        def wrapper(func, *args, **kwargs):
            correct_path = self._modernize_path(path)

            key = (correct_path, 'POST')

            self._paths[key] = func

        return wrapper

    def put(self, path: str):
        def wrapper(func, *args, **kwargs):
            correct_path = self._modernize_path(path)

            key = (correct_path, 'PUT')

            self._paths[key] = func

        return wrapper

    def patch(self, path: str):
        def wrapper(func, *args, **kwargs):
            correct_path = self._modernize_path(path)

            key = (correct_path, 'PATCH')

            self._paths[key] = func

        return wrapper

    def delete(self, path: str):
        def wrapper(func, *args, **kwargs):
            correct_path = self._modernize_path(path)

            key = (correct_path, 'DELETE')

            self._paths[key] = func

        return wrapper
