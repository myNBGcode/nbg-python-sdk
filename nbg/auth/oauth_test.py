from unittest import mock
import urllib

from requests import Request
import pytest

from . import oauth


@pytest.fixture
def client() -> oauth.OAuthClientMixin:
    """
    Return a prepared client based on OAuthClientMixin with client_id,
    client_secret and access_token set.
    """
    client = oauth.OAuthClientMixin()
    client.scopes = ["test_scope"]
    client.client_id = "client-id-used-for-testing"
    client.client_secret = "client-secret-used-for-testing"
    client.set_access_token("access-token-used-for-testing")
    return client


class DummyRequest(Request):
    headers = {}

    def __init__(self):
        pass


def test_access_token_auth():
    """
    Ensure that the AccessTokenAuth class sets the appropriate Authorization
    header.
    """
    access_token = "a-super-mysterious-access-token"
    request = DummyRequest()
    auth_instance = oauth.AccessTokenAuth(access_token)
    processed_request = auth_instance(request)

    assert processed_request.headers["Authorization"] == f"Bearer {access_token}"


def test_oauth_client_access_token(client):
    """
    Ensure that access tokens can be set and read successfully on the client
    via a public method and property accordingly.
    """
    access_token = "this-is-used-for-testing"
    client.set_access_token(access_token)

    assert client.access_token == access_token

    access_token_2 = "another-access-token-for-testing"
    dummy_access_token_response = {"access_token": access_token_2}

    with mock.patch(
        "nbg.auth.oauth.OAuthClientMixin._exchange_authorization_code",
        return_value=dummy_access_token_response,
    ):
        client.set_access_token_from_authorization_code(
            "the-authorization-code-you-got"
        )
        assert client.access_token == access_token_2


def test_oauth_client_request_auth(client):
    """
    Ensure that OAuth client returns the appropriate auth instance for use in
    requests.
    """
    auth = client.request_auth

    assert isinstance(auth, oauth.AccessTokenAuth)
    assert client.request_auth.access_token == client.access_token


def test_oauth_client_get_authorization_code_url(client):
    """
    Ensure that the `get_authorization_code_url` method of the client returns
    the appropriate URL.
    """
    redirect_uri = "https://redirect.local"
    encoded_redirect_uri = urllib.parse.quote(redirect_uri, safe="")
    scope = urllib.parse.quote(" ".join(client.scopes))
    url = client.get_authorization_code_url(redirect_uri)
    expected_url = (
        f"https://my.nbg.gr/identity/connect/authorize?"
        f"client_id={client.client_id}&redirect_uri={encoded_redirect_uri}&"
        f"scope={scope}&response_type=code"
    )
    assert url == expected_url
