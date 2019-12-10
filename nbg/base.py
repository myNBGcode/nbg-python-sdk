import uuid

from requests import Request, Response, Session
from requests.auth import AuthBase
import requests

from . import exceptions


class AccessTokenAuth(requests.auth.AuthBase):
    def __init__(self, access_token: str):
        self.access_token = access_token

    def __call__(self, request):
        request.headers["Authorization"] = f"Bearer {self.access_token}"
        return request


class BaseClient(Session):
    _base_url = ""
    _production_base_url = ""
    _sandbox_base_url = ""

    _scopes = []
    _production_scopes = []
    _sandbox_scopes = []

    def __init__(self, client_id: str, client_secret: str, production: bool = False):
        super().__init__()
        self.client_id = client_id
        self.client_secret = client_secret
        self.production = production

        self._base_url = (
            self._production_base_url if production else self._sandbox_base_url
        )
        self._scopes = self._production_scopes if production else self._sandbox_scopes

    def _prepare_request_headers(
        self, request_id: str, method: str, data: dict
    ) -> dict:
        headers = {}
        headers["Client-Id"] = self.client_id
        headers["Request-Id"] = request_id
        return headers

    def _prepare_request_body(self, request_id: str, method: str, data: dict) -> dict:
        body = {
            "header": {"ID": request_id, "application": self.client_id},
            "payload": data,
        }
        return body

    def _prepare_request_auth(self, method: str, data: dict) -> AccessTokenAuth:
        return AccessTokenAuth(self._access_token)

    def _process_response(self, response: Response) -> dict:
        data = response.json()

        if data.get("exception"):
            raise exceptions.ResponseException(response)

        return data["payload"]

    def _api_request(self, method: str, url_path: str, data: dict = {}) -> dict:
        request_id = str(uuid.uuid4())
        headers = self._prepare_request_headers(request_id, method, data)
        body = self._prepare_request_body(request_id, method, data)
        auth = self._prepare_request_auth(method, data)
        url = f"{self._base_url}/{url_path}"
        response = self.request(method, url, headers=headers, auth=auth, json=body)
        return self._process_response(response)

    def get_authorization_code_url(
        self, redirect_uri: str, scope: str = None, response_type: str = "code"
    ):
        _scope = scope or " ".join(self._scopes)
        params = {
            "client_id": self.client_id,
            "redirect_uri": redirect_uri,
            "scope": _scope,
            "response_type": response_type,
        }
        request = Request(
            "GET", "https://my.nbg.gr/identity/connect/authorize", params=params
        )
        prepared_request = request.prepare()
        return prepared_request.url

    def exchange_authorization_code_with_token(self, authorization_code: str):
        response = requests.post(
            "https://my.nbg.gr/identity/connect/token",
            headers={"cache-control": "no-cache"},
            data={
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "grant_type": "authorization_code",
                "code": authorization_code,
                "redirect_uri": "https://developer.nbg.gr/oauth2/redoc-callback",
            },
        )
        return response

    def set_access_token(self, access_token: str):
        self._access_token = access_token
