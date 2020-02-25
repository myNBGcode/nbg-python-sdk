"""
Utilities for authorising requests, based on the consents framework.
"""

from . import oauth, signature


class ConsentClient(oauth.OAuthClientMixin, signature.SignedClientMixin):
    """
    Base class for managing consents and authorising requests based on the
    consents framework.
    """

    @property
    def consent_id(self):
        """
        Return the consent ID of the current client.
        """
        return self._consent_id

    @property
    def consent_headers(self) -> dict:
        """
        Return the required headers for authorising a request with a consent.
        """
        check_consent = self.production
        x_consent_check = "true" if check_consent else "false"
        consent_id = getattr(self, "_consent_id")
        headers = {"X-Consent-Check": x_consent_check}

        if check_consent and consent_id:
            headers["Consent-Id"] = consent_id

        return headers

    def set_consent_id(self, consent_id: str):
        """
        Set the consent ID for the current client.
        """
        self._consent_id = consent_id

    def generate_consent(self) -> dict:
        """
        Generate a consent ID for use by the current client.
        """
        data = {"applicationId": self.application_id}
        headers = [self.environment_headers, self.signature_headers]
        return self._api_request("POST", "consents/request-access", data, headers)

    def get_consent_information(self, consent_id: str, user_id: str) -> dict:
        """
        Returns information for the requested consent.
        """
        data = {
            "applicationId": self.client_id,
            "userId": user_id,
            "consentId": consent_id,
        }
        headers = [self.environment_headers, self.signature_headers]
        return self._api_request("POST", "consents/info", data, headers)

    def delete_consent(self, consent_id: str, user_id: str, tan_number: str) -> dict:
        """
        Delete the requested consent.
        """
        data = {"userId": user_id, "consentId": consent_id, "tanNumber": tan_number}
        headers = [self.environment_headers, self.signature_headers]
        return self._api_request("POST", "consents/delete", data, headers)
