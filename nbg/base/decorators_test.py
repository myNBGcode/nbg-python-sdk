from . import decorators, resources


class DummyResource(resources.BaseResource):
    a: int
    b: str


class DummyAPI:
    @decorators.api_call
    def dummy_method(self) -> DummyResource:
        return {"a": "1", "b": 2}


def test_decorator_response_to_resource():
    """
    Ensure that the `api_call` decorator will successfully transform a
    valid JSON response to the corresponding API resource, based on each
    method's return type hint.
    """
    dummy_client = DummyAPI()
    dummy_resource = dummy_client.dummy_method()

    assert isinstance(dummy_resource, DummyResource)
    assert dummy_resource.a == 1
    assert dummy_resource.b == "2"
