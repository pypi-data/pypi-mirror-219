from __future__ import annotations

import asyncio
import re
import sqlite3
import time
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any, Sequence, cast

import aiosqlite
import orjson
from pydantic import BaseModel

from beni import bfunc, block, bpath
from beni.btype import Null

sqlite3.register_converter(
    "bool",
    lambda x: x not in (
        b'',
        b'0',
        # None, # 如果是None根本就不会进来，这里判断也没有意义
    )
)

_ALIVE = 5 * 60  # 数据库链接至少存活时间（因为清除不是实时执行）


class SqliteDb:

    def __init__(self, file: str | Path, max_num: int = 10):
        self._ary: asyncio.Queue[_SqliteDbWrite] = asyncio.Queue()
        self.lock = block.RWLock(max_num)
        self._file = bpath.get(file)
        self._rtime_dict: dict[int, float] = {}  # rtime = release time
        asyncio.create_task(self._clean())

    def exists(self):
        return self._file.exists()

    async def _clean(self):
        while True:
            await asyncio.sleep(_ALIVE)
            now = time.monotonic()
            ary: list[_SqliteDbWrite] = []
            while not self._ary.empty():
                db = self._ary.get_nowait()
                db_key = id(db)
                release_time = self._rtime_dict[db_key]
                if now - release_time > _ALIVE:
                    del self._rtime_dict[db_key]
                    await db.close()
                else:
                    ary.append(db)
            for db in ary:
                self._ary.put_nowait(db)

    async def close(self, write_lock: bool = True):
        if write_lock:
            await self.lock.get_write()
        while not self._ary.empty():
            db = self._ary.get_nowait()
            await db.close()
        if write_lock:
            self.lock.release_write()

    async def _get_db(self):
        if self._ary.empty():
            db = _SqliteDbWrite()
            await db.connect(self._file)
        else:
            db = self._ary.get_nowait()
        return db

    def _release_db(self, db: _SqliteDbWrite):
        self._rtime_dict[id(db)] = time.monotonic()
        self._ary.put_nowait(db)

    @asynccontextmanager
    async def _use_db(self):
        db = await self._get_db()
        try:
            yield db
        finally:
            self._release_db(db)

    @asynccontextmanager
    async def read(self):
        async with self.lock.use_read():
            async with self._use_db() as db:
                yield cast(_SqliteDbRead, db)

    @asynccontextmanager
    async def write(self):
        async with self.lock.use_write():
            async with self._use_db() as db:
                try:
                    yield db
                    await db.commit()
                except:
                    await db.rollback()
                    raise

    async def add(self, table: str, data: dict[str, Any]):
        async with self.write() as db:
            return await db.add(table, data)

    async def add_ary(self, table: str, ary: list[dict[str, Any]]):
        async with self.write() as db:
            return await db.add_ary(table, ary)

    async def update(self, table: str, data: dict[str, Any], statement: str = '', *args: Any):
        async with self.write() as db:
            return await db.update(table, data, statement, *args)

    async def get(self, sql: str, *args: Any):
        async with self.read() as db:
            return await db.get(sql, *args)

    async def get_ary(self, sql: str, *args: Any):
        async with self.read() as db:
            return await db.get_ary(sql, *args)

    async def value(self, sql: str, *args: Any):
        async with self.read() as db:
            return await db.value(sql, *args)

    async def execute(self, sql: str, *args: Any):
        async with self.write() as db:
            return await db.execute(sql, *args)


class _SqliteDbRead:

    _db: aiosqlite.Connection = Null

    async def connect(self, file: Path | str):
        self._db = await aiosqlite.connect(file, detect_types=sqlite3.PARSE_DECLTYPES)
        self._db.row_factory = sqlite3.Row

    async def close(self):
        await self._db.close()

    async def get(self, sql: str, *args: Any):
        async with self._db.execute(sql, args) as cursor:
            return await cursor.fetchone()

    async def get_ary(self, sql: str, *args: Any):
        async with self._db.execute(sql, args) as cursor:
            return cast(list[sqlite3.Row], await cursor.fetchall())

    async def value(self, sql: str, *args: Any):
        row = await self.get(sql, *args)
        assert row
        return row[0]


class _SqliteDbWrite(_SqliteDbRead):

    async def add(self, table: str, data: dict[str, Any]):
        keys = sorted(data.keys())
        names = ','.join([f'"{x}"' for x in keys])
        values = [data[x] for x in keys]
        async with self._db.execute(
            f'''
            INSERT INTO `{table}` ({names})
            VALUES
                {bfunc.get_sql_placement(keys)}
            ''',
            values,
        ) as cursor:
            return cursor.lastrowid

    async def add_ary(self, table: str, ary: list[dict[str, Any]]):
        keyset: set[str] = set()
        for data in ary:
            keyset.update(data.keys())
        keys = sorted(keyset)
        names = ','.join([f'`{x}`' for x in keys])
        values = [[data.get(key) for key in keys] for data in ary]
        async with self._db.executemany(
            f'''
            INSERT INTO `{table}` ({names})
            VALUES
                {bfunc.get_sql_placement(keys)}
            ''',
            values
        ) as cursor:
            return cursor.rowcount

    async def update(self, table: str, data: dict[str, Any], statement: str = '', *args: Any):
        keys = sorted(data.keys())
        names = ','.join([f'`{x}`=?' for x in keys])
        values = [data[x] for x in keys] + list(args)
        async with self._db.execute(
            f'''
            UPDATE `{table}`
            SET {names}
            {statement}
            ''',
            values,
        ) as cursor:
            return cursor.rowcount

    async def execute(self, sql: str, *args: Any):
        async with self._db.execute(sql, args) as cursor:
            return cursor.rowcount

    async def commit(self):
        return await self._db.commit()

    async def rollback(self):
        return await self._db.rollback()


_RE_TABLE = re.compile(r'(.*?)Model$')


class SqliteDbModel(BaseModel):

    __table__ = ''

    _db: SqliteDb = Null

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson.dumps

    @classmethod
    def set_db(cls, db: SqliteDb):
        cls._db = db

    @classmethod
    def get_db(cls):
        return cls._db

    @classmethod
    @property
    def TABLE(cls):
        if not cls.__table__:
            name: str = _RE_TABLE.findall(cls.__name__)[0]
            name_ary = list(name)
            name_ary[0] = name_ary[0].lower()
            for i in range(len(name_ary)):
                v = name_ary[i]
                if v.isupper():
                    name_ary[i] = f'_{v.lower()}'
            result = ''.join(name_ary)
            cls.__table__ = result
        return cls.__table__

    async def add(self):
        return await self._add()

    async def _add(self, exclude: set[str] | None = None, include: set[str] | None = None):
        return await self._db.add(
            self.TABLE,
            self.dict(
                exclude=cast(Any, exclude),
                include=cast(Any, include),
            )
        )

    @classmethod
    async def add_ary(cls, ary: Sequence[SqliteDbModel]):
        return await cls._add_ary(ary)

    @classmethod
    async def _add_ary(cls, ary: Sequence[SqliteDbModel], exclude: set[str] | None = None):
        if not ary:
            return 0
        return await cls._db.add_ary(
            cls.TABLE,
            [x.dict(exclude=exclude) for x in ary],
        )

    async def _update(self, statement: str = '', *args: Any, exclude: set[str] | None = None, include: set[str] | None = None):
        return await self._db.update(
            self.TABLE,
            self.dict(
                exclude=exclude,
                include=include,
            ),
            statement,
            *args,
        )

    @classmethod
    async def remove_all(cls):
        return await cls._db.execute(
            f'DELETE FROM {cls.TABLE}',
        )

    @classmethod
    async def _remove(cls, statement: str = '', *args: Any):
        return await cls._db.execute(
            f'DELETE FROM {cls.TABLE} {statement}',
            *args,
        )

    @classmethod
    async def _get(cls, statement: str = '', *args: Any, fields: set[str] | None = None):
        row = await cls._db.get(
            f'''
            SELECT
                {fields and ', '.join(fields) or '*'}
            FROM
                `{cls.TABLE}`
            {statement}
            LIMIT 1
            ''',
            *args,
        )
        if row:
            return cls(**dict(row))

    @classmethod
    async def _get_ary(cls, statement: str = '', *args: Any, fields: set[str] | None = None):
        rows = await cls._db.get_ary(
            f'''
            SELECT
                {fields and ', '.join(fields) or '*'}
            FROM
                `{cls.TABLE}`
            {statement}
            ''',
            *args,
        )
        return [cls(**dict(x)) for x in rows]

    @classmethod
    async def _count(cls, statement: str = '', *args: Any) -> int:
        return await cls._db.value(
            f'''
            SELECT
                COUNT( * )
            FROM
                `{cls.TABLE}`
            {statement}
            ''',
            *args,
        )
