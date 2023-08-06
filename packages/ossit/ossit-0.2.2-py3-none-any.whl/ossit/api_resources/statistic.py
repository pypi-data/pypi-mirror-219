from ..api_requestor import APIRequestor
from ..config import config


VALID_METHODS = ('set', 'increment', 'decrement', 'add', 'subtract')


class Statistic(APIRequestor):
    endpoint_path = 'statistics'

    @classmethod
    def add(cls, group: str,  statistic: str, value: float, reference_date: str = None):
        return cls.update(group, statistic, value, reference_date, method='add')

    @classmethod
    def create(cls, group: str, name: str, value: float, reference_date: str = None):
        url_path = cls.generate_url_path()
        body = {
            'group': group,
            'name': name,
            'value': value,
            'reference_date': reference_date or config.local_date_str(),
        }
        return cls.post_request(url_path, body)

    @classmethod
    def delete(cls, group: str, statistic: str, reference_date: str):
        query_params = {'reference_date': reference_date}
        url_path = cls.generate_url_path(group, statistic, query_params=query_params)
        return cls.delete_request(url_path)

    @classmethod
    def decrement(cls, group, statistic, reference_date: str = None):
        return cls.update(group, statistic, 1, reference_date, method='decrement')

    @classmethod
    def increment(cls, group, statistic, reference_date: str = None):
        return cls.update(group, statistic, 1, reference_date, method='increment')

    @classmethod
    def list(cls):
        url_path = cls.generate_url_path()
        return cls.get_request(url_path)

    @classmethod
    def purge(cls, group: str, statistic: str):
        query_params = {'purge': True}
        url_path = cls.generate_url_path(group, statistic, query_params=query_params)
        return cls.delete_request(url_path)

    @classmethod
    def retrieve(cls, group: str, statistic: str):
        url_path = cls.generate_url_path(group, statistic)
        return cls.get_request(url_path)

    @classmethod
    def subtract(cls, group: str,  statistic: str, value: float, reference_date: str = None):
        return cls.update(group, statistic, value, reference_date, method='subtract')

    @classmethod
    def update(cls, group: str, statistic: str, value: float, reference_date: str = None, method: str = 'set'):
        if method not in VALID_METHODS:
            raise ValueError(f'Invalid method: {method}')

        url_path = cls.generate_url_path(group, statistic)
        body = {
            'group': group,
            'name': statistic,
            'value': value,
            'reference_date': reference_date or config.local_date_str(),
            'method': method,
        }
        return cls.post_request(url_path, body)


class StatisticGroup(APIRequestor):
    endpoint_path = 'statistic-groups'

    @classmethod
    def create(cls, name):
        url_path = cls.generate_url_path()
        body = {'name': name}
        return cls.post_request(url_path, body)

    @classmethod
    def delete(cls, group):
        url_path = cls.generate_url_path(group)
        return cls.delete_request(url_path)

    @classmethod
    def list(cls):
        url_path = cls.generate_url_path()
        return cls.get_request(url_path)

    @classmethod
    def retrieve(cls, group):
        url_path = cls.generate_url_path(group)
        return cls.get_request(url_path)

    @classmethod
    def update(cls, group, name):
        url_path = cls.generate_url_path(group)
        return cls.post_request(url_path, {'name': name})
