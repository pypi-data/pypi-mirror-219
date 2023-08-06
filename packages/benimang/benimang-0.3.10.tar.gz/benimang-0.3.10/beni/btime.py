import datetime as xdatetime
import time as xtime

from beni import bhttp

_server_time: float = xtime.time()
_init_time: float = xtime.monotonic()


async def network():
    _, response = await bhttp.get('https://www.baidu.com')
    date_str = response.headers['Date']
    return xdatetime.datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S GMT') + xdatetime.timedelta(hours=8)


async def init_server_time():
    global _server_time, _init_time
    _server_time = (await network()).timestamp()
    _init_time = xtime.monotonic()


def timestamp():
    return _server_time + xtime.monotonic() - _init_time


def timestamp_sec():
    return int(timestamp())


def timestamp_millsec():
    return int(timestamp() * 1000)


def datetime():
    return xdatetime.datetime.fromtimestamp(timestamp())


def date():
    return xdatetime.date.fromtimestamp(timestamp())


def time():
    return datetime().time()


def datetime_str(fmt: str = r'%Y-%m-%d %H:%M:%S'):
    return datetime().strftime(fmt)


def date_str(fmt: str = r'%Y-%m-%d'):
    return date().strftime(fmt)


def time_str(fmt: str = r'%H:%M:%S'):
    return time().strftime(fmt)


def make_datetime(date_str: str, fmt: str = r'%Y-%m-%d %H:%M:%S'):
    return xdatetime.datetime.strptime(date_str, fmt)


def make_date(date_str: str, fmt: str = r'%Y-%m-%d'):
    return xdatetime.datetime.strptime(date_str, fmt).date()
