from .api_resources import *
from .ossit_response import OssitResponse
from .config import config
from .utils import *


def set_domain_key(domain_key):
    config.domain_key = domain_key


def set_time_zone(time_zone):
    config.TIME_ZONE = time_zone
