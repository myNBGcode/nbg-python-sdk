import os

import pytest

from . import signature


@pytest.fixture
def client():
    return signature.SignedClientMixin()


def test_nbg_certificate(client):
    """
    Ensure that the signed client always returns the appropriate NBG
    certificate.
    """
    current_dir = os.path.dirname(__file__)
    certs_dir = os.path.join(current_dir, "certs")
    client.production = True

    with open(os.path.join(certs_dir, "nbg-qseal-production.cer"), "rb") as certificate:
        assert client.nbg_certificate == certificate.read()

    client.production = False

    with open(os.path.join(certs_dir, "nbg-qseal-sandbox.cer"), "rb") as certificate:
        assert client.nbg_certificate == certificate.read()


def test_tpp_certificate(client):
    """
    Ensure that the TPP certificate can be set and read successfully on the client
    via a public method and property accordingly.
    """
    tpp_certificate = "this-should-be-a-tpp-certificate"
    client.set_tpp_certificate(tpp_certificate)

    assert client.tpp_certificate == tpp_certificate


def test_tpp_private_key(client):
    """
    Ensure that the TPP private_key can be set and read successfully on the client
    via a public method and property accordingly.
    """
    tpp_private_key = "this-should-be-a-tpp-private-key"
    client.set_tpp_private_key(tpp_private_key)

    assert client.tpp_private_key == tpp_private_key

@pytest.mark.skip(reason="Request signing has not been implemented yet.")
def test_signature_headers():
    """
    Ensure that `SignedClientMixin` generates the appropriate HTTP headers for
    the provided request body.
    """
    pass


@pytest.mark.skip(reason="Verifying signed responses has not been implemented yet.")
def test_verify_response():
    """
    Ensure that `SignedClientMixin` can successfully verify a signed response.
    """
    pass