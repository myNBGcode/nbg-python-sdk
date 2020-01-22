"""
Utilities for authenticating requests based on OAuth 2 and OpenID Connect.
"""

from requests import Request
from requests.auth import AuthBase
import requests


class AccessTokenAuth(requests.auth.AuthBase):
    """
    Authentication class, based on the `requests` library, for use by the
    a client to authenticate requests with an access token.
    """
    def __init__(self, access_token: str):
        self.access_token = access_token

    def __call__(self, request):
        request.headers["Authorization"] = f"Bearer {self.access_token}"
        return request


class OAuthClientMixin:
    """
    Enables implementation of NBG API clients that can authenticate requests
    based on OAuth2 access tokens.
    """
    client_id: str
    client_secret: str
    scopes: str

    def _exchange_authorization_code(self, authorization_code: str) -> dict:
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
        return response.json()

    @property
    def access_token(self) -> str:
        """
        Returns the access token of the current client.
        """
        return self._access_token

    @property
    def request_auth(self) -> AccessTokenAuth:
        """
        Returns the `requests` authentication instance for the current client.
        """
        return AccessTokenAuth(self.access_token)

    def get_authorization_code_url(
        self, redirect_uri: str, scope: str = None, response_type: str = "code"
    ) -> str:
        """
        Composes and returns the URL that has to be visited by a user to
        get an authorization code for the current client.
        """
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

    def set_access_token(self, access_token: str):
        """
        Sets the access token for the current client.
        """
        self._access_token = access_token

    def set_access_token_from_authorization_code(self, authorization_code: str):
        """
        Exchanges an authorization code with an access token and sets the
        access token accordingly for the current client.
        """
        access_token_response = self._exchange_authorization_code(authorization_code)
        self.set_access_token(access_token_response["access_token"])
