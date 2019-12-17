from requests import Request

from . import auth


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
    auth_instance = auth.AccessTokenAuth(access_token)
    processed_request = auth_instance(request)

    assert processed_request.headers["Authorization"] == f"Bearer {access_token}"
