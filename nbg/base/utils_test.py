from datetime import datetime
import json

from requests import Response
import pytest

from . import exceptions, utils


def _get_dummy_response(body, status_code=200) -> Response:
    body_encoding = "utf-8"
    body_string = body if isinstance(body, str) else json.dumps(body)
    body_bytes = bytes(body_string, body_encoding)
    response = Response()
    response.status_code = status_code
    response.encoding = body_encoding
    response._content = body_bytes
    return response


def test_serialize_request_payload():
    datetime_to_serialize = datetime(1906, 12, 9)
    serialized_datetime = "1906-12-09T00:00:00.000Z"
    payload = {"dateFrom": datetime_to_serialize}
    desired_serialized_payload = {"dateFrom": "1906-12-09T00:00:00.000Z"}
    serialized_payload = utils.serialize_request_payload(payload)

    assert serialized_payload == desired_serialized_payload


def test_validate_response_with_valid_response():
    response_body = {"payload": {"msg": "I am so valid!"}}
    valid_response = _get_dummy_response(response_body)
    validated_response = utils.validate_response(valid_response)

    assert validated_response == response_body


def test_validate_response_with_401_status_code():
    response_body = ""
    invalid_response = _get_dummy_response(response_body, status_code=401)

    with pytest.raises(exceptions.NotAuthenticatedRequest) as exception_info:
        utils.validate_response(invalid_response)

    assert exception_info.value.response == invalid_response


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
