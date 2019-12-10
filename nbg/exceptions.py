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
