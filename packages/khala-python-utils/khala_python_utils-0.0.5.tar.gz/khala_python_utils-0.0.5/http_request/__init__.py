import requests
from requests.auth import HTTPBasicAuth


class Request:
    def __init__(self, url: str, auth: dict = None):
        self.url = url
        if auth is not None:
            self.auth = HTTPBasicAuth(auth['username'], auth['password'])

    def get(self, params=None, **kwargs):
        kwargs.setdefault('auth', getattr(self, 'auth', None))
        return requests.get(self.url, params, **kwargs).json()

    def post(self, json=None, data=None, **kwargs):
        kwargs.setdefault('auth', getattr(self, 'auth', None))
        return requests.post(self.url, data, json, **kwargs).json()
