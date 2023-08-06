from pathlib import Path
from typing import Any, Callable
from zipfile import ZIP_DEFLATED, ZipFile

from beni import bexecute, bpath


async def zip_file(zfile: Path | str, file: Path | str, name: str | None = None):
    zfile = bpath.get(zfile)
    file = bpath.get(file)
    if name is None:
        name = file.name
    await _zip(zfile, {name: file})


async def zip_folder(zfile: Path | str, folder: Path | str, filter_func: Callable[[Path], bool] | None = None):
    zfile = bpath.get(zfile)
    folder = bpath.get(folder)
    ary = await bpath.list_path(folder, True)
    if filter_func:
        ary = list(filter(filter_func, ary))
    await _zip(zfile, {str(x.relative_to(folder)): x for x in ary})


async def unzip(zfile: Path | str, folder: Path | str | None = None):
    zfile = bpath.get(zfile)
    folder = folder or zfile.parent
    with ZipFile(zfile) as f:
        for item in sorted(f.namelist()):
            f.extract(item, folder)
            # 处理压缩包中的中文文件名在windows下乱码
            try:
                # zipfile 代码中指定了cp437，这里会导致中文乱码
                xx = item.encode('cp437').decode('gbk')
                if item != xx:
                    toFile = bpath.get(folder, xx)
                    bpath.get(folder, item).rename(toFile)
            finally:
                pass


async def _zip(zfile: Path, path_dict: dict[str, Path]):
    await bpath.make(zfile.parent)
    with ZipFile(zfile, 'w', ZIP_DEFLATED) as f:
        for fname in sorted(path_dict.keys()):
            file = path_dict[fname]
            if file.is_file():
                f.write(file, fname)


# ---------------------------------------------------------------------------------------------------------


async def seven_zip(zfile: Path | str, file: Path | str):
    await _run_seven('a', zfile, file)


async def seven_unzip(zfile: Path | str, folder: Path | str):
    await _run_seven('x', f'-o{folder}', zfile)


async def seven_rename(zfile: Path | str, src: str, dst: str):
    await _run_seven('rn', zfile, src, dst)


async def _run_seven(*args: Any):
    result_bytes, error_bytes, _ = await bexecute.run_quiet('7zr', *args)
    assert not error_bytes, error_bytes.decode('gbk')
    assert b'Everything is Ok' in result_bytes, result_bytes.decode('gbk')
