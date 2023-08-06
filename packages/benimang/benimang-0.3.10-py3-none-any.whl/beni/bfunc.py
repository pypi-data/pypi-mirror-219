import asyncio
import os
import random
import sys
import uuid
from concurrent.futures import ThreadPoolExecutor
from contextlib import asynccontextmanager
from functools import wraps
from pathlib import Path
from typing import Any, Callable, Coroutine, cast

import async_timeout

from beni.btype import AnyType, AsyncFunc, IntFloatStr, Null


def sys_utf8():
    if sys.platform == 'win32':
        os.system('chcp 65001')


def add_env_dir(p: Path | str):
    value = os.getenv('path') or ''
    value = ';'.join([value, str(p)])
    os.putenv('path', value)


def make_verify_code(length: int):
    minValue = 10 ** (length - 1)
    maxValue = int('9' * length)
    return str(random.randrange(minValue, maxValue))


def get_inside(value: IntFloatStr, min_value: IntFloatStr, max_value: IntFloatStr):
    '包括最小值和最大值'
    value = min(value, max_value)
    value = max(value, min_value)
    return value


def get_value(value: float, min_value: float, max_value: float, min_result: float, max_result: float):
    '根据百分之计算指定数值'
    if value >= max_value:
        return max_result
    elif value <= min_value:
        return min_result
    else:
        percent = (value - min_value) / (max_value - min_value)
        return min_result + (max_result - min_result) * percent


def get_increase(fromValue: float, toValue: float):
    return toValue / fromValue - 1


def to_float(value: IntFloatStr, default: float = 0):
    result = default
    try:
        result = float(value)
    except:
        pass
    return result


def to_int(value: IntFloatStr, default: int = 0):
    result = default
    try:
        result = int(value)
    except:
        pass
    return result


def get_sql_placement(ary: list[Any] | set[Any]):
    return '(' + ','.join(['?' for _ in range(len(ary))]) + ')'


def get_wrapped(data: Any):
    result = data
    while hasattr(result, '__wrapped__'):
        result = getattr(result, '__wrapped__')
    return result


def retry(times: int):
    def fun(func: AsyncFunc) -> AsyncFunc:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any):
            current = 0
            while True:
                try:
                    return await func(*args, **kwargs)
                except:
                    current += 1
                    if current >= times:
                        raise
        return cast(AsyncFunc, wrapper)
    return fun


@asynccontextmanager
async def timeout(timeout: float):
    async with async_timeout.timeout(timeout):
        yield


def sync_call(func: Callable[..., Coroutine[Any, Any, AnyType]]) -> Callable[..., AnyType]:
    @wraps(func)
    def wraper(*args: Any, **kwargs: Any):
        return asyncio.run(func(*args, **kwargs))
    return cast(Any, wraper)


_once_call_set: set[int] = set()


def once_call(func: Callable[..., AnyType]) -> Callable[..., AnyType]:
    @wraps(func)
    def wraper(*args: Any, **kwargs: Any):
        assert id(func) not in _once_call_set, f'函数 {func.__module__}.{func.__name__} 只能调用一次'
        _once_call_set.add(id(func))
        return func(*args, **kwargs)
    return cast(Any, wraper)


def init_pretty_errors():
    import pretty_errors
    pretty_errors.configure(
        separator_character='*',
        filename_display=pretty_errors.FILENAME_COMPACT,
        # line_number_first   = True,
        display_link=True,
        lines_before=5,
        lines_after=2,
        line_color=pretty_errors.RED + '> ' + pretty_errors.default_config.line_color,
        code_color='  ' + pretty_errors.default_config.line_color,
        truncate_code=False,
        display_locals=True
    )
    # pretty_errors.blacklist('c:/python')


def Counter(value: int = 0):
    def _(v: int = 1):
        nonlocal value
        value += v
        return value
    return _


_thread_pool_exector: ThreadPoolExecutor = Null
_thread_max_workers: int = 4


def set_run_thread_max(value: int):
    global _thread_pool_exector, _thread_max_workers
    if not _thread_pool_exector:
        _thread_max_workers = value
    else:
        raise Exception('ThreadPoolExecutor 实例化之后不允许调用 set_thread_max_workers')


async def run_thread(func: Callable[..., AnyType]) -> AnyType:
    global _thread_pool_exector
    if not _thread_pool_exector:
        _thread_pool_exector = ThreadPoolExecutor(max_workers=_thread_max_workers)
    return await asyncio.get_running_loop().run_in_executor(_thread_pool_exector, func)


def get_mac():
    return uuid.UUID(int=uuid.getnode()).hex[-12:]
