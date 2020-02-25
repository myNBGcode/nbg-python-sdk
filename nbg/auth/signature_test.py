from unittest import mock
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
    Ensure that the TPP private_key can be set and read successfully on the
    client via a public method and property accordingly.
    """
    tpp_private_key = "secret-key"
    client.set_tpp_private_key(tpp_private_key)

    assert client.tpp_private_key == tpp_private_key


def test_signature_headers(client):
    """
    Ensure that `SignedClientMixin` generates the appropriate HTTP headers for
    the provided request body.
    """
    request_body = {}
    jws_signature = "some_header.some_payload.some_signature"
    jws_detached_signature = "some_header..some_signature"
    tpp_private_key = "secret-key"
    tpp_certificate = "this-is-a-certificate"
    expected_signature_headers = {
        "X-Certificate-Check": "true",
        "TPP-Signature-Certificate": tpp_certificate,
        "Signature": jws_detached_signature,
    }

    client.set_tpp_private_key(tpp_private_key)
    client.set_tpp_certificate(tpp_certificate)

    with mock.patch("nbg.auth.signature.SignedClientMixin.signing_enabled", True):
        with mock.patch("jose.jws.sign", return_value=jws_signature) as sign_mock:
            signature_headers = client.signature_headers(request_body)

    sign_mock.assert_called_once_with(
        request_body, tpp_private_key, algorithm="RS256",
    )
    assert signature_headers == expected_signature_headers
