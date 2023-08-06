import json
from abc import ABC
from datetime import date
import http.client
from urllib.parse import quote, urlencode, urlparse

from .ossit_response import OssitResponse
from .config import config

'''
    Not blocking request that self destroys the thread. 
'''


def encode_parameters(*args):
    for arg in args:
        if isinstance(arg, str):
            yield quote(arg)
        elif isinstance(arg, date):
            yield quote(arg.strftime("%Y-%m-%d"))
    return [quote(arg) for arg in args]


class APIRequestor(ABC):
    base_url = config.BASE_URL
    version = config.VERSION
    endpoint_path = None

    @classmethod
    def domain_key(cls):
        return config.domain_key

    @classmethod
    def create_connection(cls) -> http.client.HTTPSConnection:
        parsed_url = urlparse(cls.base_url)
        if parsed_url.scheme == "https":
            connection = http.client.HTTPSConnection(parsed_url.netloc)
        else:
            connection = http.client.HTTPConnection(parsed_url.netloc)

        return connection

    @classmethod
    def delete_request(cls, path):
        connection = cls.create_connection()
        connection.request("DELETE", path, headers=cls.headers())
        response = connection.getresponse()
        json_data = OssitResponse(response).parse_response()
        connection.close()
        return json_data

    @classmethod
    def get_request(cls, path):
        connection = cls.create_connection()
        connection.request("GET", path, headers=cls.headers())
        response = connection.getresponse()
        json_data = OssitResponse(response).parse_response()
        connection.close()
        return json_data

    @classmethod
    def post_request(cls, url, body):
        encoded_body = json.dumps(body).encode('utf-8')
        connection = cls.create_connection()
        connection.request("POST", url, encoded_body, headers=cls.headers())
        response = connection.getresponse()
        json_data = OssitResponse(response).parse_response()
        connection.close()
        return json_data

    @classmethod
    def generate_url_path(cls, *args, **kwargs):
        query_parameters = kwargs.get('query_params', {})
        path_parameters = '/'.join(encode_parameters(*args))

        url = f"/v1/api/{cls.endpoint_path}/{path_parameters}".rstrip('/')

        if query_parameters:
            query = urlencode(query_parameters)
            url += '?' + query

        return url

    @classmethod
    def headers(cls):
        return {
            "Authorization": f"Bearer {cls.domain_key()}",
            "Content-Type": "application/json",
        }

