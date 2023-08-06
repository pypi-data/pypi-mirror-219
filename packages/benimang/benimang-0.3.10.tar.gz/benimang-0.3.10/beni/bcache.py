from __future__ import annotations

import asyncio
import pickle
from datetime import datetime, timedelta
from functools import wraps
from pathlib import Path
from typing import Any, Callable, Coroutine, cast

from beni import bfile, bfunc, bhash, bpath, btime
from beni.bdefine import END_DATETIME


class Store:

    def __init__(self, cache_dir: Path) -> None:
        self._CACHE_DIR = cache_dir
        self._DEADLINE = _StoreDeadline(cache_dir)

    async def put(self, key: str, data: Any, *, duration: timedelta | None = None, deadline: datetime | None = None):
        assert not (duration and deadline), 'BCacheStore.put 不允许同时指定 duration 和 deadline'
        file = self._get_file(key)
        try:
            await bfile.write_bytes(
                file,
                pickle.dumps(data),
            )
            if not deadline:
                if duration:
                    deadline = btime.datetime() + duration
                else:
                    deadline = END_DATETIME
            self._DEADLINE.update(key, deadline)
            return True
        except:
            await bpath.remove(file)
            self._DEADLINE.clear(key)
            return False

    async def get(self, key: str):
        file = self._get_file(key)
        if file.is_file():
            if await self._DEADLINE.valid(key):
                return pickle.loads(await bfile.read_bytes(file))
            else:
                await bpath.remove(file)
        else:
            self._DEADLINE.clear(key)

    async def clear(self, key: str):
        await bpath.remove(self._get_file(key))

    def cache_func(self, key: str, *, duration: timedelta | None = None, deadline: datetime | None = None):
        def fun(func: bfunc.AsyncFunc) -> bfunc.AsyncFunc:
            @wraps(func)
            async def wrapper(*args: Any, **kwargs: Any):
                try:
                    result = await self.get(key)
                    if result is None:
                        result = await func(*args, **kwargs)
                        await self.put(key, result, duration=duration, deadline=deadline)
                    return result
                except:
                    await self.clear(key)
                    raise
            return cast(Any, wrapper)
        return fun

    def _get_file(self, key: str):
        return bpath.get(self._CACHE_DIR, bhash.crc_str(key))


class _StoreDeadline:

    def __init__(self, cache_dir: Path) -> None:
        self._file = cache_dir.joinpath('deadline.dat')
        self._writing = False
        try:
            self._data: dict[str, datetime] = pickle.loads(
                asyncio.run(bfile.read_bytes(self._file))
            )
        except:
            self._data: dict[str, datetime] = {}

    async def valid(self, key: str):
        if key in self._data:
            if self._data[key] > btime.datetime():
                return True
            else:
                self.clear(key)
        return False

    def update(self, key: str, deadline: datetime):
        self._data[key] = deadline
        self._flush()

    def clear(self, key: str):
        if key in self._data:
            del self._data[key]
            self._flush()

    def _flush(self):
        if not self._writing:
            self._writing = True
            asyncio.create_task(self._write())

    async def _write(self):
        await asyncio.sleep(2)
        self._writing = False
        try:
            await bfile.write_bytes(
                self._file,
                pickle.dumps(self._data),
            )
        except:
            pass

# ---------------------------------------------------------------------------------------------------------


def cache_func(func: bfunc.AsyncFunc) -> bfunc.AsyncFunc:
    @wraps(func)
    async def wraper(*args: Any, **kwargs: Any):
        base_func = bfunc.get_wrapped(func)
        data = _cache_dict.get(base_func)
        if not data:
            data = _CacheFuncData()
            _cache_dict[base_func] = data
        key = (args, kwargs)
        while True:
            result = data.get(key)
            if result is not None:
                return result
            elif data.running:
                await data.event.wait()
                continue
            else:
                data.running = True
                try:
                    result = await func(*args, **kwargs)
                    data.set(key, result)
                    return result
                except:
                    return None
                finally:
                    data.running = False
                    data.event.set()
                    data.event.clear()
    return cast(Any, wraper)


def cache_func_clear(func: Callable[..., _AsyncFunc]):
    base_func = bfunc.get_wrapped(func)
    data = _cache_dict.get(base_func)
    if data:
        data.clear()


class _CacheFuncData:

    def __init__(self) -> None:
        self.event = asyncio.Event()
        self.running = False
        self._result_ary: list[tuple[_FuncArgs, Any]] = []

    def get(self, key: _FuncArgs):
        for xx in self._result_ary:
            if xx[0] == key:
                return xx[1]

    def set(self, key: _FuncArgs, result: Any):
        self._result_ary = list(filter(lambda x: x[0] != key, self._result_ary))
        self._result_ary.append((key, result))

    def clear(self):
        self._result_ary.clear()


_AsyncFunc = Coroutine[Any, Any, object]
_FuncArgs = tuple[tuple[Any, ...], dict[str, Any]]  # (*args, **kwargs)
_cache_dict: dict[Callable[..., _AsyncFunc], _CacheFuncData] = {}
