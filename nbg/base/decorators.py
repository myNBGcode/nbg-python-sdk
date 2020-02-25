import inspect


def api_call(method: callable):
    """
    Mark a client method as an API call. This enables each NBG API client
    to serialise server responses, based on the provided type annotations.
    """
    method_signature = inspect.signature(method)
    response_type = method_signature.return_annotation

    def wrapper_method(*args, **kwargs):
        response_payload = method(*args, **kwargs)
        return response_type(response_payload)

    return wrapper_method
