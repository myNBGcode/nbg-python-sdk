import pytest

from . import consent


@pytest.fixture
def client():
    return consent.ConsentClient()


def test_consent_id(client):
    """
    Ensure that the consent ID can be set and read successfully on the client
    via a public method and property accordingly.
    """
    consent_id = "this-should-be-a-consent-id"
    client.set_consent_id(consent_id)

    assert client.consent_id == consent_id


def test_consent_headers(client):
    """
    Ensure that consent headers are successfully returned for the provided
    consent ID.
    """
    consent_id = "this-should-be-a-consent-id"
    client.set_consent_id(consent_id)
    client.production = True

    assert client.consent_headers == {
        "X-Consent-Check": "true",
        "Consent-Id": consent_id,
    }

    client.production = False

    assert client.consent_headers == {"X-Consent-Check": "false"}
