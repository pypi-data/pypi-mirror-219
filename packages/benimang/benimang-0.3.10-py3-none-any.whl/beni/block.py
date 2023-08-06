from __future__ import annotations

import asyncio
import inspect
from contextlib import asynccontextmanager
from functools import wraps
from pathlib import Path
from typing import Any, cast

from beni import bfunc, bhash, binput, bpath
from beni.btype import Function


@asynccontextmanager
async def file_lock(*keys: str, timeout: float = 0, quite: bool = False):
    import portalocker
    lock_ary: list[portalocker.Lock] = []
    keyfile_ary: list[Path] = []
    for key in keys:
        lock, keyfile = await _file_lock_acquire(key, timeout, quite)
        lock_ary.append(lock)
        keyfile_ary.append(keyfile)
    try:
        yield
    finally:
        for lock in lock_ary:
            lock.release()
        for keyfile in keyfile_ary:
            try:
                await bpath.remove(keyfile)
            except:
                pass


async def _file_lock_acquire(key: str, timeout: float = 0, quite: bool = False):
    '''不对外部提供，只提供给 async_keylock 方法使用'''
    keyfile = bpath.workspace(f'.lock/{bhash.crc_str(key)}.lock')
    await bpath.make(keyfile.parent)
    import portalocker
    while True:
        try:
            lock = portalocker.Lock(keyfile, timeout=timeout, fail_when_locked=timeout == 0)
            f = lock.acquire()
            f.write(key)
            f.flush()
            break
        except:
            if quite:
                raise Exception(f'资源被锁定无法继续操作 key={key} keyfile={keyfile}')
            else:
                async def __retry(_):
                    print('正在重试...')

                async def __exit(_):
                    raise Exception(f'资源被锁定无法继续操作 - {key}')

                asyncio.run(
                    binput.select(
                        binput.Selections('重试', desc='retry', handler=__retry),
                        binput.Selections('退出', desc='exit', handler=__exit),
                    )
                )
    return lock, keyfile


# ------------------------------------------------------------------------------------------------------------------------


def limit(limit: int = 1):
    def f1(func: bfunc.AsyncFunc) -> bfunc.AsyncFunc:
        @wraps(func)
        async def f2(*args: Any, **kwargs: Any):
            func_id = id(inspect.unwrap(func))
            if func_id not in _limit_dict:
                _limit_dict[func_id] = _Limit(limit)
            try:
                await _limit_dict[func_id].wait()
                return await func(*args, **kwargs)
            finally:
                await _limit_dict[func_id].release()
        return cast(Any, f2)
    return f1


async def set_limit(func: Function, limit: int):
    func_id = id(inspect.unwrap(func))
    if func_id not in _limit_dict:
        _limit_dict[func_id] = _Limit(limit)
    else:
        await _limit_dict[func_id].set_limit(limit)


_limit_dict: dict[int, _Limit] = {}


class _Limit():

    _queue: asyncio.Queue[Any]
    _running: int

    def __init__(self, limit: int):
        self._limit = limit
        self._queue = asyncio.Queue()
        self._running = 0
        while self._queue.qsize() < self._limit:
            self._queue.put_nowait(True)

    async def wait(self):
        await self._queue.get()
        self._running += 1

    async def release(self):
        if self._queue.qsize() < self._limit:
            await self._queue.put(True)
        self._running -= 1

    async def set_limit(self, limit: int):
        self._limit = limit
        while self._running + self._queue.qsize() < self._limit:
            await self._queue.put(True)
        while self._running + self._queue.qsize() > self._limit:
            if self._queue.empty():
                break
            await self._queue.get()


# ------------------------------------------------------------------------------------------------------------------------


class RWLock():

    def __init__(self, max_num: int) -> None:
        self._max_num = max_num
        self._read_num = 0
        self._write_num = 0
        self._on_read_done = asyncio.Event()
        self._on_write_done = asyncio.Event()

    async def get_read(self):
        while True:
            if self._write_num:
                await self._wait_write_done()
            elif self._read_num >= self._max_num:
                await self._wait_read_done()
            else:
                self._read_num += 1
                return

    def release_read(self):
        self._read_num -= 1
        if not self._read_num:
            self._on_read_done.set()

    @asynccontextmanager
    async def use_read(self):
        await self.get_read()
        try:
            yield
        finally:
            self.release_read()

    async def _wait_read_done(self):
        self._on_read_done.clear()
        await self._on_read_done.wait()

    async def get_write(self):
        while True:
            if self._write_num:
                await self._wait_write_done()
            elif self._read_num:
                await self._wait_read_done()
            else:
                self._write_num += 1
                return

    def release_write(self):
        self._write_num -= 1
        self._on_write_done.set()

    @asynccontextmanager
    async def use_write(self):
        await self.get_write()
        try:
            yield
        finally:
            self.release_write()

    async def _wait_write_done(self):
        self._on_write_done.clear()
        await self._on_write_done.wait()
