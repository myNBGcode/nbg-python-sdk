import json
import uuid

from requests import Request, Response, Session
from requests.auth import AuthBase
import requests

from . import auth, exceptions, utils


class BaseClient(Session, auth.AuthenticatedClientMixin):
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

    def _process_response(self, response: Response) -> dict:
        data = utils.validate_response(response)

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
