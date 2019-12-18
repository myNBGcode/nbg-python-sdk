import typing

from . import decorators, resources


class Sandbox(resources.BaseResource):
    sanboxId: str
    version: int
    users: typing.List[dict]  # TODO: implement `User`
    consentApplicationIds: typing.List[dict]  # TODO: implement `ApplicationId`
    consents: typing.List[dict]  # TODO: implement `SandboxConsentModel`


class SandboxedClientMixin:
    _production_base_url = ""
    _sandbox_base_url = ""

    _scopes = []
    _production_scopes = []
    _sandbox_scopes = []

    production: bool = False

    @property
    def base_url(self):
        _base_url = (
            self._production_base_url if self.production else self._sandbox_base_url
        )
        return _base_url

    @property
    def scopes(self):
        _scopes = self._production_scopes if self.production else self._sandbox_scopes
        return _scopes

    @decorators.api_call
    def create_sandbox(self, sandbox_id: str) -> Sandbox:
        data = {"sandboxId": sandbox_id}
        return self._api_request("POST", "sandbox", data)

    @decorators.api_call
    def export_sandbox(self, sandbox_id: str) -> dict:
        return self._api_request("GET", "sandbox/{sandbox_id}")

    @decorators.api_call
    def import_sandbox(self, sandbox_id: str, data: dict) -> dict:
        return self._api_request("PUT", "sandbox/{sandbox_id}", data)

    @decorators.api_call
    def delete_sandbox(self, sandbox_id: str) -> bool:
        return self._api_request("DELETE", f"sandbox/{sandbox_id}")

    def set_sandbox(self, sandbox_id: str):
        self._sandbox_id = sandbox_id

    def append_sandbox_headers(self, headers: dict) -> dict:
        headers["sandbox_id"] = self._sandbox_id
        return headers
