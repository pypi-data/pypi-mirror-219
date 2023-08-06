import binascii
import hashlib
import json
from pathlib import Path
from typing import Any

import aiofiles


def json_dumps(value: Any):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'))


def md5_bytes(data: bytes):
    return hashlib.md5(data).hexdigest()


def md5_str(data: str):
    return md5_bytes(data.encode())


def md5_data(data: Any):
    return md5_str(
        json_dumps(data)
    )


async def md5_file(file: Path | str):
    return md5_bytes(
        await _read_bytes(file)
    )


def crc_bytes(data: bytes):
    return hex(binascii.crc32(data))[2:].zfill(8)


def crc_str(data: str):
    return crc_bytes(data.encode())


def crc_data(data: Any):
    return crc_str(
        json_dumps(data)
    )


async def crc_file(file: Path | str):
    return crc_bytes(
        await _read_bytes(file)
    )


async def _read_bytes(file: Path | str):
    '''避免直接使用bfile导致循环引用'''
    async with aiofiles.open(file, 'rb') as f:
        return await f.read()
