"""
Utilities for managing NBG API requests to both production and sandbox
environments.
"""

import typing

from . import decorators


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

    _production_consent_base_url = ""
    _sandbox_consent_base_url = ""

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
    def consent_base_url(self):
        """
        Returns the consent base URL of the current client according to the configured
        environment.
        """
        _base_url = (
            self._production_consent_base_url
            if self.production
            else self._sandbox_consent_base_url
        )
        query = f"consent_id={self.consent_id}"

        if not self.production:
            query = f"{query}&sandbox_id={self._sandbox_id}"

        return f"{_base_url}?{query}"

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

    def create_sandbox(self, sandbox_id: str) -> dict:
        """
        Create a sandbox with the given ``sandbox_id``.

        :param sandbox_id: The unique ID of the sandbox to be created.
        :type sandbox_id: string

        ---
        **Usage**

        .. code-block:: python

            client.create_sandbox("my-unique-sandbox-id")
        """
        data = {"sandboxId": sandbox_id}
        return self._api_request("POST", "sandbox", data)

    def export_sandbox(self, sandbox_id: str) -> dict:
        """
        Returns all contents of the sandbox identified by the given `sandbox_id`.

        :param sandbox_id: The unique ID of the sandbox to get its data.
        :type sandbox_id: string

        ---
        **Usage**

        .. code-block:: python

            client.export_sandbox("my-unique-sandbox-id")
        """
        return self._api_request("GET", f"sandbox/{sandbox_id}")

    def import_sandbox(self, sandbox_id: str, data: dict) -> dict:
        """
        Imports the given `data` into the sandbox identified by the given `sandbox_id`.

        :param sandbox_id: The unique ID of the sandbox into which to import data.
        :type sandbox_id: string
        :param data: The JSON data to import into the sandbox
        :type data: dict

        ---
        **Usage**

        .. code-block:: python

            sandbox_data = {"sandbox": "data", "key": "value"}
            client.import_sandbox("my-unique-sandbox-id", sandbox_data)
        """
        return self._api_request("PUT", f"sandbox/{sandbox_id}", data)

    def delete_sandbox(self, sandbox_id: str) -> bool:
        """
        Deletes the sandbox identified by the given `sandbox_id`.

        :param sandbox_id: The unique ID of the sandbox to delete.
        :type sandbox_id: string

        ---
        **Usage**

        .. code-block:: python

            client.delete_sandbox("my-unique-sandbox-id")
        """
        return self._api_request("DELETE", f"sandbox/{sandbox_id}")

    def set_sandbox(self, sandbox_id: str):
        """
        Sets the sandbox ID to be used by the current client.

        :param sandbox_id: The unique ID of the sandbox to use in subsequent
                           API requests.
        :type sandbox_id: string

        ---
        **Usage**

        .. code-block:: python

            client.set_sandbox("my-unique-sandbox-id")
        """
        self._sandbox_id = sandbox_id
