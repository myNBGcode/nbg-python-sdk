import inspect

from . import exceptions


class BaseResource:
    def __init__(self, payload):
        members = inspect.getmembers(self)
        annotations = [value for key, value in members if key == "__annotations__"][0]
        missing_arguments = []

        for annotation_name, annotation_type in annotations.items():
            default_value = getattr(self, annotation_name, None)
            has_default_value = hasattr(self, annotation_name)

            if not has_default_value and annotation_name not in payload:
                missing_arguments.append([annotation_name, annotation_type])
                continue

            value = annotation_type(payload.get(annotation_name, default_value))
            setattr(self, annotation_name, value)

        if len(missing_arguments):
            raise exceptions.MissingResourceArguments(self.__class__, missing_arguments)

    def __getitem__(self, key):
        return getattr(self, key)
