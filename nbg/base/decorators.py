import inspect


def api_call(original_method):
    original_method_signature = inspect.signature(original_method)
    response_type = original_method_signature.return_annotation

    def wrapper_method(*args, **kwargs):
        response_payload = original_method(*args, **kwargs)
        return response_type(response_payload)

    return wrapper_method
