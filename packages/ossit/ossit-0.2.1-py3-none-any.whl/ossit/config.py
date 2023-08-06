from datetime import datetime
from zoneinfo import ZoneInfo


class OssitConfig:
    domain_key = None
    BASE_URL = 'https://ossit.ca'
    # BASE_URL = 'http://127.0.0.1:8000'
    VERSION = '0.1.0'
    TIME_ZONE = 'America/Edmonton'

    def local_date(self):
        time_zone = ZoneInfo(self.TIME_ZONE)
        return datetime.now(time_zone).date()

    def local_date_str(self):
        time_zone = ZoneInfo(self.TIME_ZONE)
        return datetime.now(time_zone).strftime('%Y-%m-%d')

    def local_datetime(self):
        time_zone = ZoneInfo(self.TIME_ZONE)
        return datetime.now(time_zone)


config = OssitConfig()
