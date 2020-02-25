"""
Exceptions to used by the base client of all NBG APIs.
"""

import re

from requests import Response


class InvalidResponse(Exception):
    """
    This exception is being raised when an invalid response was received by
    the server.
    """

    def __init__(self, response: Response, message: str):
        self.response = response
        self.message = message

    def __str__(self):
        return f"{self.message}"


class GenericResponseError(Exception):
    """
    This exception is being raised when the JSON response received by the
    server indicates that a generic error has taken place.
    """

    descriptions = {
        "1.1.0": "Only POST method is allowed",
        "1.1.1": "Header Error : Header is NULL",
        "2.1.2": "Header Error : Header is NULL",
        "1.1.3": "Header Error : Application is NULL",
        "1.2": "Model state is invalid",
        "C.0.0": "Action not allowed for CORPORATE users",
        "C.0.1": "Action not allowed for CORPORATE users",
        "2.1.1": "Request body is null",
        "2.2.1": "UserId is null",
        "2.2.3": "Inconsistent User ID",
        "3.1.1": "header.ID/header.application must be valid GUIDs",
    }

    def __init__(self, response: Response):
        self.response = response
        self.body = response.json()
        self.message = self.body["Message"]

        code_pattern_match = re.match(r"Error ([1-9A-Z.]+)$", self.message)

        if code_pattern_match is None:
            raise InvalidResponse(response, "Invalid generic error code message.")

        self.code = code_pattern_match.groups()[0]
        self.description = (
            self.descriptions[self.code]
            if self.code in self.descriptions
            else "Unknown generic error code"
        )


class ResponseException(Exception):
    """
    This exception is being raised when the JSON response received by the
    server indicates that an exception has been raised.
    """

    def __init__(self, response: Response):
        self.response = response

        json_data = response.json()["exception"]

        self.id = json_data["id"]
        self.sev = json_data["sev"]
        self.description = json_data["desc"]
        self.category = json_data["cat"]
        self.code = json_data["code"]

    def __str__(self):
        return f"[{self.code}] {self.description}"


class MissingResourceArguments(Exception):
    """
    This exception is being raised when the JSON object does not contain all
    required fields, as defined in the corresponding resource.
    """

    def __init__(self, resource_class, missing_arguments):
        self.resource_class = resource_class
        self.missing_arguments = missing_arguments

    def __str__(self):
        missing_arguments_str = ", ".join(
            [
                f"{argument_name} ({argument_type})"
                for argument_name, argument_type in self.missing_arguments
            ]
        )
        return f"{self.resource_class} cannot be created, as the following payload arguments were not provided: {missing_arguments_str}."
