from ..api_requestor import APIRequestor
from ..config import config


class Domain(APIRequestor):
    endpoint_path = 'domains'

    @classmethod
    def create(cls, name):
        url_path = cls.generate_url_path()
        body = {'name': name}
        return cls.post_request(url_path, body)

    @classmethod
    def delete(cls):
        url_path = cls.generate_url_path(config.domain_key)
        return cls.delete_request(url_path)

    @classmethod
    def list(cls):
        url_path = cls.generate_url_path()
        return cls.get_request(url_path)

    @classmethod
    def retrieve(cls):
        url_path = cls.generate_url_path(config.domain_key)
        return cls.get_request(url_path)

    @classmethod
    def update(cls, name):
        url_path = cls.generate_url_path(config.domain_key)
        return cls.post_request(url_path, {'name': name})
