"""
Generic utilities used by the base client of all NBG APIs.
"""

import json

from requests import Request, Response

from . import exceptions


def validate_response(response: Response) -> dict:
    """
    Validates that the given response is valid JSON and it contains all required
    fields.
    """
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
