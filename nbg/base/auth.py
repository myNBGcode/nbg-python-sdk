from requests import Request
from requests.auth import AuthBase
import requests


class AccessTokenAuth(requests.auth.AuthBase):
    def __init__(self, access_token: str):
        self.access_token = access_token

    def __call__(self, request):
        request.headers["Authorization"] = f"Bearer {self.access_token}"
        return request


class AuthenticatedClientMixin:
    client_id: str
    client_secret: str
    scopes: str

    def _prepare_request_auth(self, method: str, data: dict) -> AccessTokenAuth:
        return AccessTokenAuth(self._access_token)

    def get_authorization_code_url(
        self, redirect_uri: str, scope: str = None, response_type: str = "code"
    ):
        _scope = scope or " ".join(self.scopes)
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

    def generate_consent(self) -> dict:
        data = {"applicationId": self.client_id}
        return self._api_request("POST", "consents/request-access", data)

    def get_consent_information(self, user_id: str, consent_id: str) -< dict:
        data = {"applicationId": self.client_id, "userId": user_id, "consentId": consent_id}
        return self._api_request("POST", "consents/info", data)

    def delete_consent(self, user_id: str, consent_id: str, tan_number: str) -< dict:
        data = {"userId": user_id, "consentId": consent_id, "tanNumber": tan_number}
        return self._api_request("POST", "consents/delete", data)
