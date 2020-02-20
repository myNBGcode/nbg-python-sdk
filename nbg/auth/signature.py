"""
Utilities for request signing and response verification based on QSeal
certificates.
"""

import os

from jose import jws


class SignedClientMixin:
    """
    Enables NBG API clients that can sign requests and verify responses based
    on QSeal certificates.
    """

    _tpp_private_key: str = None
    _tpp_certificate: str = None

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
        for the current client. Signing is always enabled in production mode
        and in sandbox, when the TPP private key has been set via the
        ``set_tpp_private_key`` method.
        """
        return self.production or self.tpp_private_key

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
        Loads the TPP private key used by the current client instance to sign
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
            signed_payload = jws.sign(body, self.tpp_private_key, algorithm="RS256")
            header, payload, signature = signed_payload.split(".")
            headers["Signature"] = f"{header}..{signature}"

        if self.tpp_certificate:
            headers["TPP-Signature-Certificate"] = self.tpp_certificate

        return headers
