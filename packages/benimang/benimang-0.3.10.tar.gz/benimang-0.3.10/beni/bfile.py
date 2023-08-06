from pathlib import Path
from typing import Any

import aiofiles

from beni import bhash, block, bpath

_limit = 50


@block.limit(_limit)
async def write_text(file: Path | str, content: str, encoding: str = 'utf8', newline: str = '\n'):
    file = bpath.get(file)
    await bpath.make(file.parent)
    async with aiofiles.open(file, 'w', encoding=encoding, newline=newline) as f:
        return await f.write(content)


@block.limit(_limit)
async def write_bytes(file: Path | str, data: bytes):
    file = bpath.get(file)
    await bpath.make(file.parent)
    async with aiofiles.open(file, 'wb') as f:
        return await f.write(data)


@block.limit(_limit)
async def write_yaml(file: Path | str, data: Any):
    import yaml
    await write_text(file, yaml.safe_dump(data))


@block.limit(_limit)
async def write_json(file: Path | str, data: Any, mini: bool = True):
    if mini:
        await write_text(file, bhash.json_dumps(data))
    else:
        import json
        await write_text(file, json.dumps(data, ensure_ascii=False, sort_keys=True, indent=4))


@block.limit(_limit)
async def read_text(file: Path | str, encoding: str = 'utf8', newline: str = '\n'):
    async with aiofiles.open(file, 'r', encoding=encoding, newline=newline) as f:
        return await f.read()


@block.limit(_limit)
async def read_bytes(file: Path | str):
    async with aiofiles.open(file, 'rb') as f:
        return await f.read()


@block.limit(_limit)
async def read_yaml(file: Path | str):
    import yaml
    return yaml.safe_load(
        await read_text(file)
    )


@block.limit(_limit)
async def read_json(file: Path | str):
    import orjson
    return orjson.loads(await read_bytes(file))


@block.limit(_limit)
async def read_toml(file: Path | str):
    import tomllib
    return tomllib.loads(
        await read_text(file)
    )
