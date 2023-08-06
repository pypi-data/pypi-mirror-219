import json


class OssitResponse:
    def __init__(self, response):
        self.response = response

    def parse_response(self):
        # Todo: Read status code of the response.
        return json.loads(self.response.read().decode("utf-8"))

