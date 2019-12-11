import typing

import pytest

from . import exceptions, resources


class DummyResource(resources.BaseResource):
    some_str_arg: str = "some default text"
    some_int_arg: int
    some_bool_arg: bool
    some_dict_arg: dict


class DummyParentResource(resources.BaseResource):
    some_nested_dummy_resource: DummyResource
    another_int_arg: int


class DummyResourceWithListAttribute(resources.BaseResource):
    a_list_of_integers: typing.List[int]


def test_resource_correct_init_with_arguments():
    payload = {
        "some_str_arg": "lorem",
        "some_int_arg": 5,
        "some_bool_arg": False,
        "some_dict_arg": {"a": "b"},
    }
    resource = DummyResource(payload)

    assert resource.some_str_arg == "lorem"
    assert resource.some_int_arg == 5
    assert resource.some_bool_arg == False
    assert resource.some_dict_arg == {"a": "b"}


def test_resource_correct_init_with_arguments_conversion():
    payload = {
        "some_str_arg": 42,
        "some_int_arg": "1",
        "some_bool_arg": 1,
        "some_dict_arg": {"a": "b"},
    }
    resource = DummyResource(payload)

    assert resource.some_str_arg == "42"
    assert resource.some_int_arg == 1
    assert resource.some_bool_arg == True
    assert resource.some_dict_arg == {"a": "b"}


def test_resource_dict_type_arguments():
    payload = {
        "some_str_arg": "lorem",
        "some_int_arg": 5,
        "some_bool_arg": False,
        "some_dict_arg": {"a": "b"},
    }
    resource = DummyResource(payload)

    assert resource["some_str_arg"] == "lorem"
    assert resource["some_int_arg"] == 5
    assert resource["some_bool_arg"] == False
    assert resource["some_dict_arg"] == {"a": "b"}


def test_resource_default_arguments():
    payload = {"some_int_arg": 4, "some_bool_arg": True, "some_dict_arg": {"a": "b"}}
    resource = DummyResource(payload)

    assert resource.some_str_arg == "some default text"
    assert resource.some_int_arg == 4
    assert resource.some_bool_arg == True
    assert resource.some_dict_arg == {"a": "b"}


def test_resource_missing_arguments():
    payload = {"some_str_arg": "hey"}

    with pytest.raises(exceptions.MissingResourceArguments) as exception_info:
        resource = DummyResource(payload)

    assert exception_info.value.resource_class == DummyResource
    assert exception_info.value.missing_arguments == [
        ["some_int_arg", int],
        ["some_bool_arg", bool],
        ["some_dict_arg", dict],
    ]


def test_resource_with_nested_resources():
    payload = {
        "some_nested_dummy_resource": {
            "some_str_arg": "ipsum",
            "some_int_arg": 314,
            "some_bool_arg": True,
            "some_dict_arg": {"c": "d"},
        },
        "another_int_arg": 42,
    }
    resource = DummyParentResource(payload)

    assert resource.some_nested_dummy_resource.some_str_arg == "ipsum"
    assert resource.some_nested_dummy_resource.some_int_arg == 314
    assert resource.some_nested_dummy_resource.some_bool_arg == True
    assert resource.some_nested_dummy_resource.some_dict_arg == {"c": "d"}
    assert resource.another_int_arg == 42


def test_resource_with_list_attribute():
    payload = {"a_list_of_integers": [1, "2", 3.8]}
    resource = DummyResourceWithListAttribute(payload)

    assert resource.a_list_of_integers == [1, 2, 3]
