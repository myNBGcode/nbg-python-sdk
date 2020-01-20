import pytest

from . import environment


@pytest.fixture
def dummy_client() -> environment.EnvironmentClientMixin:
    client = environment.EnvironmentClientMixin()
    client._production_base_url = "https://production-base-url.nbg.gr"
    client._sandbox_base_url = "https://sandbox-base-url.nbg.dev"
    client._production_scopes = ["scope1", "scope2"]
    client._sandbox_scopes = ["scope3", "scope4", "scope5"]
    return client


def test_sandboxed_base_url(dummy_client: environment.EnvironmentClientMixin):
    dummy_client.production = True
    assert dummy_client.base_url == dummy_client._production_base_url

    dummy_client.production = False
    assert dummy_client.base_url == dummy_client._sandbox_base_url


def test_sandboxed_scopes(dummy_client: environment.EnvironmentClientMixin):
    dummy_client.production = True
    assert dummy_client.scopes == dummy_client._production_scopes

    dummy_client.production = False
    assert dummy_client.scopes == dummy_client._sandbox_scopes


def test_set_sandbox(dummy_client: environment.EnvironmentClientMixin):
    sandbox_id = "magnificent-sandbox-id"
    dummy_client.set_sandbox(sandbox_id)

    assert dummy_client._sandbox_id == sandbox_id


def test_append_sandbox_headers(dummy_client: environment.EnvironmentClientMixin):
    sandbox_id = "amazing-sandbox-id"
    dummy_client.set_sandbox(sandbox_id)
    headers = {"Authorization": "Bearer: ThisIsOneToken"}

    processed_headers = dummy_client.append_sandbox_headers(headers)
    assert headers == processed_headers
    assert headers["sandbox_id"] == sandbox_id
