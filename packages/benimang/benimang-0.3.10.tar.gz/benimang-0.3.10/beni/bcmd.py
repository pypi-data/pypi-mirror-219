import asyncio
import json
import os
import sys
import time
from datetime import datetime as Datetime
from datetime import timezone
from enum import Enum
from pathlib import Path
from typing import Optional
from zoneinfo import ZoneInfo

import nest_asyncio
import pyperclip
import typer
from colorama import Fore

from beni import bcolor, bexecute, bfile, binput, bpath
from beni.btype import Null

_app = typer.Typer()


def main():
    nest_asyncio.apply()
    _app()


def exit(errorMsg: str):
    print(errorMsg)
    sys.exit(errorMsg and 1 or 0)


# ------------------------------------------------------------------------


@_app.command('time')
def showtime(
    value1: str = typer.Argument('', help='时间戳（整形或浮点型）或日期（格式: 2021-11-23）', show_default=False, metavar='[Timestamp or Date]'),
    value2: str = typer.Argument('', help='时间（格式: 09:20:20），只有第一个参数为日期才有意义', show_default=False, metavar='[Time]')
):
    '''
    格式化时间戳\n
    beni time\n
    beni time 1632412740\n
    beni time 1632412740.1234\n
    beni time 2021-9-23\n
    beni time 2021-9-23 09:47:00\n
    '''
    timestamp: float = Null
    if not value1:
        timestamp = time.time()
    else:
        try:
            timestamp = float(value1)
        except:
            try:
                if value2:
                    timestamp = Datetime.strptime(f'{value1} {value2}', '%Y-%m-%d %H:%M:%S').timestamp()
                else:
                    timestamp = Datetime.strptime(f'{value1}', '%Y-%m-%d').timestamp()
            except:
                pass

    if timestamp is None:
        color = typer.colors.BRIGHT_RED
        typer.secho('参数无效', fg=color)
        typer.secho('\n可使用格式: ', fg=color)
        msg_ary = str(showtime.__doc__).strip().replace('\n\n', '\n').split('\n')[1:]
        msg_ary = [x.strip() for x in msg_ary]
        typer.secho('\n'.join(msg_ary), fg=color)
        raise typer.Abort()

    print()
    print(timestamp)
    print()
    localtime = time.localtime(timestamp)
    tzname = time.tzname[(time.daylight and localtime.tm_isdst) and 1 or 0]
    bcolor.printx(time.strftime('%Y-%m-%d %H:%M:%S %z', localtime), tzname, colors=[Fore.YELLOW])
    print()

    # pytz版本，留作参考别删除
    # tzNameList = [
    #     'Asia/Tokyo',
    #     'Asia/Kolkata',
    #     'Europe/London',
    #     'America/New_York',
    #     'America/Chicago',
    #     'America/Los_Angeles',
    # ]
    # for tzName in tzNameList:
    #     tz = pytz.timezone(tzName)
    #     print(Datetime.fromtimestamp(timestamp, tz).strftime(fmt), tzName)

    datetime_utc = Datetime.fromtimestamp(timestamp, tz=timezone.utc)
    tzname_list = [
        'Australia/Sydney',
        'Asia/Tokyo',
        'Asia/Kolkata',
        'Africa/Cairo',
        'Europe/London',
        'America/Sao_Paulo',
        'America/New_York',
        'America/Chicago',
        'America/Los_Angeles',
    ]
    for tzname in tzname_list:
        datetime_tz = datetime_utc.astimezone(ZoneInfo(tzname))
        dstStr = ''
        dst = datetime_tz.dst()
        if dst:
            dstStr = f'(DST+{dst})'
        print(f'{datetime_tz} {tzname} {dstStr}')

    print()

# ------------------------------------------------------------------------


@_app.command('json')
def format_json():
    '''格式化 JSON （使用复制文本）'''
    import pyperclip
    content = pyperclip.paste()
    try:
        data = json.loads(content)
        print(
            json.dumps(data, indent=4, ensure_ascii=False, sort_keys=True)
        )
    except:
        bcolor.print_red('无效的 JSON')
        bcolor.print_red(content)


# ------------------------------------------------------------------------

class _MirrorType(str, Enum):
    pip = 'pip'
    npm = 'npm'
    all = 'all'


_mirror_files = {
    _MirrorType.pip: (
        bpath.user('pip/pip.ini'),
        [
            '[global]',
            'index-url = https://mirrors.aliyun.com/pypi/simple',
        ],
    ),
    _MirrorType.npm: (
        bpath.user('.bashrc'),
        [
            'registry=https://registry.npm.taobao.org/',
            'electron_mirror=https://npm.taobao.org/mirrors/electron/',
        ],
    ),
}


@_app.command()
def mirror(
    type: _MirrorType = typer.Option(_MirrorType.all, help="设置镜像的类型，支持pip/npm/all"),
    enabled: bool = typer.Option(True, help="是否使用镜像"),
):
    '''设置镜像地址'''
    async def _():
        if type is _MirrorType.all:
            type_ary = [_MirrorType.pip, _MirrorType.npm]
        else:
            type_ary = [type]
        for target_type in type_ary:
            file, msg_ary = _mirror_files[target_type]
            if enabled:
                msg = '\n'.join(msg_ary)
                await bfile.write_text(file, msg)
                bcolor.print_green('写入文件', file)
                bcolor.print_magenta(msg)
            else:
                await bpath.remove(file)
                bcolor.print_red('删除文件', file)
    asyncio.run(_())


# ------------------------------------------------------------------------

@_app.command()
def venv(
    packages: list[str] = typer.Argument(None),
    path: Path = typer.Option(None, help="指定路径，默认当前目录"),
    clear: bool = typer.Option(False, help='删除venv目录后重新安装，可以保证环境干净'),
    clear_all: bool = typer.Option(False, help='删除venv.lock文件和venv目录后重新安装，可以保证环境干净的情况下将包更新'),
):
    '''python 虚拟环境配置'''
    path = path or Path(os.getcwd())
    clear = clear or clear_all

    async def _():
        venv_dir = bpath.get(path, 'venv')
        assert_dir(venv_dir)
        if not venv_dir.exists():
            await binput.confirm('指定目录为非venv目录，是否确认新创建？')
        if clear:
            await bpath.remove(venv_dir)
        if not venv_dir.exists():
            await bexecute.run(f'python.exe -m venv {venv_dir}')
        venv_list_file = bpath.get(path, 'venv.list')
        assert_file(venv_list_file)
        if not venv_list_file.exists():
            await bfile.write_text(venv_list_file, '')
        await tidy_venv_file(venv_list_file, packages)
        venv_lock_file = bpath.get(path, 'venv.lock')
        assert_file(venv_lock_file)
        if clear_all:
            await bpath.remove(venv_lock_file)
        elif venv_lock_file.exists():
            await tidy_venv_file(venv_lock_file, packages)
        target_file = venv_lock_file if venv_lock_file.exists() else venv_list_file
        pip = bpath.get(venv_dir, 'Scripts/pip.exe')
        await pip_install(pip, target_file)
        await bexecute.run(f'{pip} freeze > {venv_lock_file}')

    async def pip_install(pip: Path, file: Path):
        python = pip.with_name('python.exe')
        assert python.is_file()
        assert pip.is_file()
        assert not await bexecute.run(f'{python} -m pip install --upgrade pip'), '更新 pip 失败'
        assert not await bexecute.run(f'{pip} install -r {file}'), '执行失败'

    async def tidy_venv_file(file: Path, packages: list[str]):
        packages_names = [get_package_name(x) for x in packages]
        ary = (await bfile.read_text(file)).strip().replace('\r\n', '\n').replace('\r\n', '\n').split('\n')
        ary = list(filter(lambda x: get_package_name(x) not in packages_names, ary))
        ary.extend(packages)
        ary.sort()
        await bfile.write_text(file, '\n'.join(ary).strip())

    def get_package_name(value: str):
        sep_ary = ['>', '<', '=']
        for sep in sep_ary:
            if sep in value:
                return value.split(sep)[0]
        return value

    def assert_file(file: Path):
        assert file.is_file() or not file.exists(), f'必须是文件 {file=}'

    def assert_dir(folder: Path):
        assert folder.is_dir() or not folder.exists(), f'必须是目录 {folder=}'

    asyncio.run(_())


# ------------------------------------------------------------------------


@_app.command()
def bin(
    name: str = typer.Argument(None, help="如果有多个使用,分割"),
    is_file: bool = typer.Option(False, '--is-file', '-f', help="文件形式指定参数，行为单位"),
    ak: str = typer.Option(..., help="七牛云账号AK"),
    sk: str = typer.Option(..., help="七牛云账号SK"),
    output: Optional[Path] = typer.Option(None, '--output', '-o', help="本地保存路径")
):
    '''从七牛云下载执行文件'''

    async def _():
        try:
            from beni.bqiniu import QiniuBucket
            nonlocal output
            bucketName = 'pytask'
            bucketUrl = 'http://qiniu-cdn.pytask.com'
            if output is None:
                output = Path(os.curdir)
            bucket = QiniuBucket(bucketName, bucketUrl, ak, sk)
            targetList: list[str] = []
            if is_file:
                content = await bfile.read_text(Path(name))
                targetList.extend(content.replace('\r\n', '\n').split('\n'))
            else:
                targetList.extend(name.strip().split(','))
            for target in targetList:
                file = output.joinpath(target).resolve()
                if file.exists():
                    print(f'exists {file}')
                else:
                    key = f'bin/{target}.zip'
                    await bucket.download_unzip(key, output)
                    bcolor.print_green(f'added  {file}')
        except Exception as e:
            print(e)

    asyncio.run(_())


# ------------------------------------------------------------------------


@_app.command()
def proxy(
    port: int = typer.Option(15236, help="代理服务器端口"),
):
    '''生成终端设置代理服务器的命令'''
    msg = '\r\n'.join([
        f'set http_proxy=http://localhost:{port}',
        f'set https_proxy=http://localhost:{port}',
        f'set all_proxy=http://localhost:{port}',
        '',
    ])
    bcolor.print_magenta('\r\n' + msg)
    pyperclip.copy(msg)
    bcolor.print_yellow('已复制，可直接粘贴使用')


# ------------------------------------------------------------------------

@_app.command()
def btask(path: str = typer.Option(None, help="项目路径")):
    '''生成 btask 项目'''

    content_dict = {
        # ------------------------------------
        'main.py':
        '''
from beni import bpath, btask


def init():
    btask.init(
        key='LOCK_KEY',
        bin_dir=bpath.get(__file__, './../../bin'),
    )


if __name__ == '__main__':
    btask.main()
        ''',
        # ------------------------------------
        'dev.py':
        '''
from beni import btask

import main

main.init()

btask.dev('hello.chicken')
# btask.dev('hello.duck')
        ''',
        # ------------------------------------
        'tasks/__init__.py':
        '''
        ''',
        # ------------------------------------
        'tasks/hello.py':
        '''
from typer import Typer
from beni import bfunc

app = Typer(help='这里是帮助信息')


@app.command()
@bfunc.sync_call
async def chicken():
    \'''chicken函数\'''
    print('我是小鸡')


@app.command()
@bfunc.sync_call
async def duck():
    \'''duck函数\'''
    print('我是小鸭')
        ''',
    }

    async def func():
        file_dir = bpath.get(path or os.getcwd())
        for key in sorted(content_dict.keys()):
            file = file_dir.joinpath(key)
            content = content_dict[key]
            await bfile.write_text(file, content)

    asyncio.run(func())
