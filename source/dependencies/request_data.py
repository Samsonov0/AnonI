import re


class RequestData:
    def __init__(self, scope, receive, path_regex, path):
        self._scope = scope
        self._receive = receive
        self._path_regex = path_regex
        self._path = path

        self._query_params: dict = dict()

    def __call__(self):
        self._set_query_params()

        return self

    def _parse_url(self):
        match = re.match(self._path_regex, self._path)

        if match:
            return match.groupdict()
        return None

    def _extract_query_params(self):
        return self._parse_url()

    def _set_query_params(self):
        self._query_params = self._extract_query_params()

    def query_params(self):
        return self._query_params
