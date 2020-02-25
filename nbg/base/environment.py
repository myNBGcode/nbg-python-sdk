"""
Utilities for managing NBG API requests to both production and sandbox
environments.
"""

import typing

from . import decorators, resources


class Sandbox(resources.BaseResource):
    sanboxId: str
    version: int
    users: typing.List[dict]  # TODO: implement `User`
    consentApplicationIds: typing.List[dict]  # TODO: implement `ApplicationId`
    consents: typing.List[dict]  # TODO: implement `SandboxConsentModel`


class EnvironmentClientMixin:
    """
    Enables sending requests to both production and sandbox APIs and also
    targeting requests to particular sandboxes.
    """

    _production_base_url = ""
    _sandbox_base_url = ""

    _scopes = []
    _production_scopes = []
    _sandbox_scopes = []

    production: bool = False

    @property
    def base_url(self):
        """
        Returns the base URL of the current client according to the configured
        environment.
        """
        _base_url = (
            self._production_base_url if self.production else self._sandbox_base_url
        )
        return _base_url

    @property
    def scopes(self):
        """
        Returns the required OAuth scopes of the current client API according
        to the configured environment.
        """
        _scopes = self._production_scopes if self.production else self._sandbox_scopes
        return _scopes

    @property
    def application_id(self):
        """
        In production mode, it returns the `client_id` of the client, or else
        it always returns `72F01708-BE1E-4567-926E-8C87D03CA551`.
        """
        return (
            self.client_id
            if self.production
            else "72F01708-BE1E-4567-926E-8C87D03CA551"
        )

    @property
    def environment_headers(self):
        """
        Returns the required headers to execute a request in the configured
        sandbox.
        """
        if hasattr(self, "_sandbox_id") and not self.production:
            return {"sandbox_id": self._sandbox_id}

        return {}

    @decorators.api_call
    def create_sandbox(self, sandbox_id: str) -> dict:
        """
        Creates a sandbox, based on the given `sandbox_id`.
        """
        data = {"sandboxId": sandbox_id}
        return self._api_request("POST", "sandbox", data)

    @decorators.api_call
    def export_sandbox(self, sandbox_id: str) -> dict:
        """
        Returns all contents of the sandbox identified by the given `sandbox_id`.
        """
        return self._api_request("GET", f"sandbox/{sandbox_id}")

    @decorators.api_call
    def import_sandbox(self, sandbox_id: str, data: dict) -> dict:
        """
        Imports the given `data` into the sandbox identified by the given `sandbox_id`.
        """
        return self._api_request("PUT", f"sandbox/{sandbox_id}", data)

    @decorators.api_call
    def delete_sandbox(self, sandbox_id: str) -> bool:
        """
        Deletes the sandbox identified by the given `sandbox_id`.
        """
        return self._api_request("DELETE", f"sandbox/{sandbox_id}")

    def set_sandbox(self, sandbox_id: str):
        """
        Sets the sandbox ID to be used by the current client.
        """
        self._sandbox_id = sandbox_id
