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
        return getattr(self, "_consent_id", None)

    @property
    def consent_headers(self) -> dict:
        """
        Return the required headers for authorising a request with a consent.
        """
        check_consent = self.consent_id is not None

        x_consent_check = "true" if check_consent else "false"
        headers = {"X-Consent-Check": x_consent_check}

        if check_consent:
            headers["Consent-Id"] = self.consent_id

        return headers

    def get_user_consent_url(self, redirect_url: str) -> str:
        """
        Get URL to present to the user to provide their consent.

        :param redirect_url: The URL to redirect to, after the consent is given
        :type redirect_url: string

        ---
        **Usage**

        .. code-block:: python

            client.get_user_consent_url(
              redirect_url="https://myapp.example.com/nbg/consent/"
            )
        """
        return f"{self.consent_base_url}&redirect_url={redirect_url}"

    def set_consent_id(self, consent_id: str):
        """
        Set the consent ID for the current client.

        :param consent_id: The consent ID from :meth:`generate_consent() <nbg.account_information.AccountInformationPSD2Client.generate_consent>`
        :type consent_id: string

        ---
        **Usage**

        .. code-block:: python

            client.set_consent_id("my-unique-consent-id")
        """
        self._consent_id = consent_id

    def generate_consent(self) -> dict:
        """
        Generate a consent ID for use by the current client.

        **Usage**

        .. code-block:: python

            client.generate_consent()
        """
        data = {"applicationId": self.application_id}
        headers = [self.environment_headers, self.signature_headers]
        return self._api_request("POST", "consents/request-access", data, headers)

    def get_consent_information(self, consent_id: str, user_id: str) -> dict:
        """
        Returns information for the requested consent.

        :param consent_id: The consent ID to get information
        :type consent_id: string

        :param user_id: The user ID of the user that provided the consent
        :type user_id: string

        ---
        **Usage**

        .. code-block:: python

            client.get_consent_information(
              consent_id="your-unique-consent-id",
              user_id="your_user_id",
            )
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

        :param consent_id: The consent ID to delete
        :type consent_id: string

        :param user_id: The user ID of the user that provided the consent
        :type user_id: string

        :param tan_number: String ``"smsotp"`` to receive TAN number on your mobile phone,
                           or the TAN number you received.
        :type tan_number: string

        ---
        **Usage**

        .. code-block:: python

            client.delete_consent(
              consent_id="your-unique-consent-id",
              user_id="your_user_id",
              tan_number="smsotp",  # Set to "smsotp" to send code you user's mobile phone
            )
            
            # After you receive the ``tan_number``.
            tan_number = "the_one_the_user_received"
            client.delete_consent(
              consent_id="your-unique-consent-id",
              user_id="your_user_id",
              tan_number=tan_number,  # Set to the code received by the user
            )
        """
        data = {"userId": user_id, "consentId": consent_id, "tanNumber": tan_number}
        headers = [self.environment_headers, self.signature_headers]
        return self._api_request("POST", "consents/delete", data, headers)
