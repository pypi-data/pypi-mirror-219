from typing import Any

from beni import bfile, bpath


async def get(key: str, default: Any = None):
    file = _get_file(key)
    if file.is_file():
        return await bfile.read_yaml(file)
    else:
        return default


async def set(key: str, value: Any):
    file = _get_file(key)
    await bfile.write_yaml(file, value)


async def remove(*args: str):
    await bpath.remove(*[_get_file(key) for key in args])


async def remove_all():
    file_ary = await bpath.list_file(_DIR)
    await bpath.remove(*file_ary)


# ------------------------------------------------------------------------------------------

_DIR = bpath.workspace('.storage')


def _get_file(key: str):
    return bpath.get(_DIR, f'{key}.yaml')
