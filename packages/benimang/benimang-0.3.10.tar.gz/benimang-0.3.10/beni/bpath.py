import os
import shutil
import sys
import uuid
from contextlib import asynccontextmanager
from pathlib import Path

from beni import bfunc


def get(path: str | Path, expand: str = ''):
    if type(path) is not Path:
        path = Path(path)
    return path.joinpath(expand).resolve()


def user(expand: str = ''):
    return get(Path('~').expanduser(), expand)


def desktop(expand: str = ''):
    return user(f'Desktop/{expand}')


def workspace(expand: str = ''):
    DIR = 'beni-workspace'
    if sys.platform == 'win32':
        return get(f'C:/{DIR}/{expand}')
    else:
        return get(f'/data/{DIR}/{expand}')


def temp_file():
    return workspace(f'temp/{uuid.uuid4()}.tmp')


def temp_dir():
    return workspace(f'temp/{uuid.uuid4()}')


def change_relative(target: Path | str, from_relative: Path | str, to_relative: Path | str):
    target = get(target)
    from_relative = get(from_relative)
    to_relative = get(to_relative)
    assert target.is_relative_to(from_relative)
    return to_relative.joinpath(target.relative_to(from_relative))


def open_dir(dir: Path | str):
    os.system(f'start explorer {dir}')


def _remove(*ary: Path | str):
    for path in ary:
        path = get(path)
        if path.is_file():
            path.unlink(True)
        elif path.is_dir():
            shutil.rmtree(path)


async def remove(*ary: Path | str):
    return await bfunc.run_thread(
        lambda: _remove(*ary)
    )


def _make(*ary: Path | str):
    for path in ary:
        path = get(path)
        path.mkdir(parents=True, exist_ok=True)


async def make(*ary: Path | str):
    return await bfunc.run_thread(
        lambda: _make(*ary)
    )


def _clear_dir(*ary: Path | str):
    for dir in ary:
        _remove(*[x for x in get(dir).iterdir()])


async def clear_dir(*ary: Path | str):
    return await bfunc.run_thread(
        lambda: _clear_dir(*ary)
    )


def _copy(src: Path | str, dst: Path | str):
    src = get(src)
    dst = get(dst)
    _make(dst.parent)
    if src.is_file():
        shutil.copyfile(src, dst)
    elif src.is_dir():
        shutil.copytree(src, dst)
    else:
        if not src.exists():
            raise Exception(f'copy error: src not exists {src}')
        else:
            raise Exception(f'copy error: src not support {src}')


async def copy(src: Path | str, dst: Path | str):
    return await bfunc.run_thread(
        lambda: _copy(src, dst)
    )


def _copy_many(data: dict[Path | str, Path | str]):
    for src, dst in data.items():
        _copy(src, dst)


async def copy_many(data: dict[Path | str, Path | str]):
    return await bfunc.run_thread(
        lambda: _copy_many(data)
    )


def _move(src: Path | str, dst: Path | str, force: bool = False):
    src = get(src)
    dst = get(dst)
    if dst.exists():
        if force:
            _remove(dst)
        else:
            raise Exception(f'move error: dst exists {dst}')
    _make(dst.parent)
    os.rename(src, dst)


async def move(src: Path | str, dst: Path | str, force: bool = False):
    return await bfunc.run_thread(
        lambda: _move(src, dst, force)
    )


def _move_many(data: dict[Path | str, Path | str], force: bool = False):
    for src, dst in data.items():
        _move(src, dst, force)


async def move_many(data: dict[Path | str, Path | str], force: bool = False):
    return await bfunc.run_thread(
        lambda: _move_many(data, force)
    )


async def move_children(src: Path | str, dst: Path | str, force: bool = False):
    for from_file in await list_path(src, True):
        to_file = change_relative(from_file, src, dst)
        await move(from_file, to_file, force)


def rename_name(src: Path | str, name: str):
    src = get(src)
    src.rename(src.with_name(name))


def rename_stem(src: Path | str, stemName: str):
    src = get(src)
    src.rename(src.with_stem(stemName))


def rename_suffix(src: Path | str, suffixName: str):
    src = get(src)
    src.rename(src.with_suffix(suffixName))


def _list_path(path: Path | str, recursive: bool = False):
    path = get(path)
    if recursive:
        return list(path.glob('**/*'))
    else:
        return list(path.glob("*"))


async def list_path(path: Path | str, recursive: bool = False):
    '''获取指定路径下文件以及目录列表'''
    return await bfunc.run_thread(
        lambda: _list_path(path, recursive)
    )


def _list_file(path: Path | str, recursive: bool = False):
    path = get(path)
    if recursive:
        return list(filter(lambda x: x.is_file(), path.glob('**/*')))
    else:
        return list(filter(lambda x: x.is_file(), path.glob('*')))


async def list_file(path: Path | str, recursive: bool = False):
    '''获取指定路径下文件列表'''
    return await bfunc.run_thread(
        lambda: _list_file(path, recursive)
    )


def _list_dir(path: Path | str, recursive: bool = False):
    path = get(path)
    if recursive:
        return list(filter(lambda x: x.is_dir(), path.glob('**/*')))
    else:
        return list(filter(lambda x: x.is_dir(), path.glob('*')))


async def list_dir(path: Path | str, recursive: bool = False):
    '''获取指定路径下目录列表'''
    return await bfunc.run_thread(
        lambda: _list_dir(path, recursive)
    )


@asynccontextmanager
async def use_temp_file():
    file = temp_file()
    try:
        yield file
    finally:
        await remove(file)


@asynccontextmanager
async def use_temp_dir(is_make: bool = False):
    path = temp_dir()
    if is_make:
        await make(path)
    try:
        yield path
    finally:
        await remove(path)


@asynccontextmanager
async def use_dir(path: str | Path):
    path = Path(path)
    currentPath = os.getcwd()
    try:
        os.chdir(str(path))
        yield
    finally:
        os.chdir(currentPath)
