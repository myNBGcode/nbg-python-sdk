"""
NBG base client module. This is used internally to create clients for all
supported NBG APIs.
"""

import json
import typing
import uuid

from requests import Request, Response, Session
from requests.auth import AuthBase
import requests

from . import environment, exceptions, utils
from ..auth import consent


LIST_OF_DICTS = typing.List[dict]
DICT_OR_LIST_OF_DICTS = typing.Union[dict, LIST_OF_DICTS]


class BaseClient(
    Session, consent.ConsentClient, environment.EnvironmentClientMixin,
):
    def __init__(self, client_id: str, client_secret: str, production: bool = False):
        super().__init__()
        self.client_id = client_id
        self.client_secret = client_secret
        self.production = production

    def _prepare_request_headers(self, request_id: str) -> dict:
        headers = {"Request-Id": request_id}

        return headers

    def _prepare_request_body(self, request_id: str, method: str, data: dict) -> dict:
        body = {
            "header": {"ID": request_id, "application": self.client_id},
            "payload": data,
        }
        return body

    def _process_response(self, response: Response) -> dict:
        self.verify_response(response)
        data = utils.validate_response(response)

        if data.get("Message"):
            raise exceptions.GenericResponseError(response)

        if data.get("exception"):
            raise exceptions.ResponseException(response)

        return data["payload"]

    def _api_request(
        self,
        method: str,
        url_path: str,
        data: dict = {},
        headers: DICT_OR_LIST_OF_DICTS = {},
    ) -> dict:
        request_id = str(uuid.uuid4())
        body = self._prepare_request_body(request_id, method, data)
        auth = self.request_auth

        _headers = {"Request-Id": request_id, "Client-Id": self.client_id}
        list_of_headers = [headers] if isinstance(headers, dict) else headers

        for header_set in list_of_headers:
            if callable(header_set):
                header_set = header_set(body)

            _headers.update(header_set)

        url = f"{self.base_url}/{url_path}"
        response = self.request(method, url, headers=_headers, auth=auth, json=body)
        return self._process_response(response)
