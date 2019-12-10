from requests import Response


class ResponseException(Exception):
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
