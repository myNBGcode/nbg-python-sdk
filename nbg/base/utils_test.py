import json

from requests import Response
import pytest

from . import exceptions, utils


def _get_dummy_response(body) -> Response:
    body_encoding = "utf-8"
    body_string = body if isinstance(body, str) else json.dumps(body)
    body_bytes = bytes(body_string, body_encoding)
    response = Response()
    response.encoding = body_encoding
    response._content = body_bytes
    return response


def test_validate_response_with_valid_response():
    response_body = {"payload": {"msg": "I am so valid!"}}
    valid_response = _get_dummy_response(response_body)
    validated_response = utils.validate_response(valid_response)

    assert validated_response == response_body


def test_validate_response_with_missing_keys():
    response_body = {"no_payload": "or_exception_either"}
    invalid_response = _get_dummy_response(response_body)

    with pytest.raises(exceptions.InvalidResponse) as exception_info:
        utils.validate_response(invalid_response)

    message = (
        "Invalid response body. "
        "The following keys are missing: exception, payload, Message."
    )

    assert str(exception_info.value) == message


def test_validate_response_with_invalid_json():
    response_body = "I am not JSON"
    invalid_response = _get_dummy_response(response_body)

    with pytest.raises(exceptions.InvalidResponse) as exception_info:
        utils.validate_response(invalid_response)

    assert str(exception_info.value) == "Response body is not valid JSON."
