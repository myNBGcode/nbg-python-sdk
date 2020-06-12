"""
Generic utilities used by the base client of all NBG APIs.
"""

from datetime import datetime
import json

from requests import Request, Response

from . import exceptions


def _serialize_datetime(datetime_instance: datetime) -> str:
    iso_datetime = datetime_instance.isoformat(timespec="milliseconds")
    return f"{iso_datetime}Z"


def serialize_request_payload(data: dict) -> dict:
    """
    Serializes the request payload to match the format requested by
    NBG APIs. Serializations:
      - datetime: (Z-suffixed ISO format)
    """
    payload = data.copy()

    for key, value in payload.items():
        if isinstance(value, datetime):
            payload[key] = _serialize_datetime(value)

    return payload


def validate_response(response: Response) -> dict:
    """
    Validates that the given response is valid JSON and it contains all required
    fields.
    """
    if response.status_code == 401:
        raise exceptions.NotAuthenticatedRequest(response)

    try:
        data = response.json()
    except json.JSONDecodeError:
        exception = exceptions.InvalidResponse(
            response, "Response body is not valid JSON."
        )
        raise exception

    required_keys = ("exception", "payload", "Message")
    any_of_the_required_keys_in_body = any([key in data for key in required_keys])

    if not any_of_the_required_keys_in_body:
        missing_keys = ", ".join([key for key in required_keys if key not in data])
        exception = exceptions.InvalidResponse(
            response,
            f"Invalid response body. The following keys are missing: {missing_keys}.",
        )
        raise exception

    return data
