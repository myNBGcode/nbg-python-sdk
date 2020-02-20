"""
Exceptions used by the authentication framework of the NBG APIs.
"""


class OAuthTokenException(Exception):
    """
    This exception is being raised when an authorisation code cannot be
    exchanged with an access token.
    """

    message: str
    original_exception: Exception

    def __init__(self, message: str, original_exception: Exception):
        self.message = message
        self.original_exception = original_exception

    def __str__(self):
        return self.message
