from requests import Response, Session
from requests.auth import AuthBase


class BaseClient(Session):
    _base_url = None
    _production_base_url = None
    _sandbox_base_url = None

    def __init__(self, client_id: str, client_secret: str, production: bool = False):
        super().__init__()
        self.client_id = client_id
        self.client_secret = client_secret
        self.production = production

        self._base_url = (
            self._production_base_url if production else self._sandbox_base_url
        )

    def _prepare_request_headers(self, method: str, data: dict) -> dict:
        raise NotImplementedError()

    def _prepare_request_auth(self, method: str, data: dict) -> AuthBase:
        raise NotImplementedError

    def _prepare_request_body(self, method: str, data: dict) -> dict:
        raise NotImplementedError()

    def _process_response(self, response: Response) -> json:
        raise NotImplementedError

    def _api_request(self, method: str, url_path: str, data: dict) -> dict:
        headers = self._prepare_request_headers(method, data)
        auth = self._prepare_request_auth(method, data)
        body = self._prepare_request_body(method, data)
        url = f"{self._base_url}/{url_path}"
        response = self.request(method, url, headers=headers, auth=auth, json=body)

        return self._process_response(response)

    def set_access_token(self, access_token: str):
        raise NotImplementedError()

    def create_sandbox(self, sandbox_id: str):
        raise NotImplementedError()

    def set_default_sandbox(self, sandbox_id: str):
        raise NotImplementedError()

    def set_consent_id(self, consent_id: str):
        raise NotImplementedError()
