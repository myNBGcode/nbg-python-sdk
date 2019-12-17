from . import sandbox


def test_sandboxed_base_url():
    dummy_client = sandbox.SandboxedClientMixin()
    dummy_client._production_base_url = "https://production-base-url.nbg.gr"
    dummy_client._sandbox_base_url = "https://sandbox-base-url.nbg.dev"

    dummy_client.production = True
    assert dummy_client.base_url == dummy_client._production_base_url

    dummy_client.production = False
    assert dummy_client.base_url == dummy_client._sandbox_base_url


def test_sandboxed_scopes():
    dummy_client = sandbox.SandboxedClientMixin()
    dummy_client._production_scopes = ["scope1", "scope2"]
    dummy_client._sandbox_scopes = ["scope3", "scope4", "scope5"]

    dummy_client.production = True
    assert dummy_client.scopes == dummy_client._production_scopes

    dummy_client.production = False
    assert dummy_client.scopes == dummy_client._sandbox_scopes
