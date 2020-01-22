"""
Utilities for request signing and response verification based on QSeal
certificates.
"""

import os


class SignedClientMixin:
    """
    Enables NBG API clients that can sign requests and verify responses based
    on QSeal certificates.
    """

    @property
    def nbg_certificate(self):
        """
        Returns the NBG certificate used to verify responses according
        to the configured environment (production or sandbox).
        """
        environment = "production" if self.production else "sandbox"
        certificate_file_name = f"nbg-qseal-{environment}.cer"
        certificate_file_path = os.path.join(
            os.path.dirname(__file__), "certs", certificate_file_name,
        )

        with open(certificate_file_path, "rb") as certificate_file:
            return certificate_file.read()

    @property
    def signing_enabled(self):
        """
        Returns whether request signing and response verification is enabled
        for the current client.
        """
        return self.production

    @property
    def tpp_private_key(self):
        """
        Returns the current client's TPP private key, used to sign requests.
        """
        return self._tpp_private_key

    @property
    def tpp_certificate(self):
        """
        Returns the current client's TPP certificate, used by the server to
        verify signed requests by the current client.
        """
        return self._tpp_certificate

    def set_tpp_private_key(self, tpp_private_key: str):
        """
        Set the TPP private key used by the current client instance to sign
        requests to the server.
        """
        self._tpp_private_key = tpp_private_key

    def set_tpp_certificate(self, tpp_certificate: str):
        """
        Set the TPP certificate used by the server to verify requests by the
        current client instance.
        """
        self._tpp_certificate = tpp_certificate

    def signature_headers(self, body: dict) -> dict:
        """
        Return the required QSeal signature headers, based on the provided
        request body.
        """
        headers = {"X-Certificate-Check": "true" if self.signing_enabled else "false"}

        if self.signing_enabled:
            headers["Signature"] = "not-implemented"  # TODO: Implement this

        if hasattr(self, "_signature_certificate"):
            headers["TPP-Signature-Certificate"] = self.tpp_certificate

        return headers

    def verify_response(self, response) -> bool:
        """
        Verify response based on the current NBG Certificate.
        """
        # TODO: Implement this
        return True