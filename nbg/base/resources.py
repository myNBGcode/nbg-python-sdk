import inspect
import typing

from . import exceptions


def type_is_list(annotation_type):
    return getattr(annotation_type, "__origin__", None) == typing.List


class BaseResource:
    def __init__(self, payload):
        members = inspect.getmembers(self)
        annotations = [value for key, value in members if key == "__annotations__"][0]
        missing_arguments = []

        for annotation_name, annotation_type in annotations.items():
            if self._argument_is_missing(annotation_name, payload):
                missing_arguments.append([annotation_name, annotation_type])
                continue

            extracted_value = self._extract_value_from_payload(annotation_name, payload)
            casted_value = self._cast_value(extracted_value, annotation_type)
            setattr(self, annotation_name, casted_value)

        if len(missing_arguments):
            raise exceptions.MissingResourceArguments(self.__class__, missing_arguments)

    def _argument_is_missing(self, argument_name, payload):
        has_default_value = hasattr(self, argument_name)
        return not has_default_value and argument_name not in payload

    def _extract_value_from_payload(self, argument_name, payload):
        default_value = getattr(self, argument_name, None)
        return payload.get(argument_name, default_value)

    def _cast_value(self, value, value_type):
        value_type_origin = getattr(value_type, "__origin__", None)
        value_type_is_list = value_type_origin in (typing.List, list)

        if value_type_is_list:
            internal_value_type = value_type.__args__[0]
            return [internal_value_type(member) for member in value]

        return value_type(value)

    def __getitem__(self, key):
        return getattr(self, key)
