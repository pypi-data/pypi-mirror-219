import asyncio
import inspect
import sys
from contextlib import asynccontextmanager
from datetime import datetime as Datetime
from pathlib import Path

import nest_asyncio
from colorama import Back, Fore
from typer import Typer

from beni import bcolor, bfunc, block, blog, bpath, btime
from beni.btype import Null

_APP = Typer()
_LOGFILE_COUNT = 100
_TASKS = 'tasks'

nest_asyncio.apply()

_key: str = 'btask'
_log_dir: Path = Null
_bin_dir: Path = Null


@bfunc.once_call
def init(
    *,
    key: str | None = None,
    log_dir: Path | str | None = None,
    bin_dir: Path | str | None = None
):
    global _key, _log_dir, _bin_dir
    if key:
        _key = key
    if log_dir:
        _log_dir = bpath.get(log_dir)
    if bin_dir:
        _bin_dir = bpath.get(bin_dir)


def main():
    async def func():
        async with _task():
            try:
                tasks_dir = _get_root_dir() / _TASKS
                files = tasks_dir.glob('*.py')
                files = filter(lambda x: not x.name.startswith('_'), files)
                for module_name in [x.stem for x in files]:
                    exec(f'import {_TASKS}.{module_name}')
                    module = eval(f'{_TASKS}.{module_name}')
                    if hasattr(module, 'app'):
                        sub: Typer = getattr(module, 'app')
                        sub.info.name = module_name.replace('_', '-')
                        _APP.add_typer(sub, name=sub.info.name)
                _APP()
            except BaseException as ex:
                if type(ex) is SystemExit and ex.code in (0, 2):
                    # 0 - 正常结束
                    # 2 - Error: Missing command.
                    pass
                else:
                    raise
    asyncio.run(func())


def dev(name: str):
    '''例：db.reverse'''
    async def func():
        async with _task():
            module, cmd = name.split('.')
            exec(f'from {_TASKS} import {module}')
            exec(f'{module}.{cmd}()')
    asyncio.run(func())


@asynccontextmanager
async def _task():
    _check_vscode_venv()
    bfunc.sys_utf8()
    if _bin_dir:
        bfunc.add_env_dir(_bin_dir)
    async with block.file_lock(_key):
        start_time = Datetime.now()
        bfunc.init_pretty_errors()
        if _log_dir:
            logfile = bpath.get(_log_dir, btime.datetime_str('%Y%m%d_%H%M%S.log'))
            assert logfile.is_file(), f'日志文件创建失败（已存在） {logfile}'
        else:
            logfile = None
        try:
            blog.init(file=logfile)
            yield
        except BaseException as ex:
            bcolor.set_colors(Fore.LIGHTRED_EX)
            blog.error(str(ex))
            blog.error('执行失败')
            raise
        finally:

            if blog.get_critical_count():
                color = Fore.LIGHTWHITE_EX + Back.LIGHTMAGENTA_EX
            elif blog.get_error_count():
                color = Fore.LIGHTWHITE_EX + Back.LIGHTRED_EX
            elif blog.get_warning_count():
                color = Fore.BLACK + Back.YELLOW
            else:
                color = Fore.BLACK + Back.LIGHTGREEN_EX

            bcolor.set_colors(color)
            blog.info('-' * 75)

            msg_ary = ['任务结束']
            if blog.get_critical_count():
                msg_ary.append(f'critical({blog.get_critical_count()})')
            if blog.get_error_count():
                msg_ary.append(f'error({blog.get_error_count()})')
            if blog.get_warning_count():
                msg_ary.append(f'warning({blog.get_warning_count()})')

            bcolor.set_colors(color)
            blog.info(' '.join(msg_ary))

            pass_time = str(Datetime.now() - start_time)
            if pass_time.startswith('0:'):
                pass_time = '0' + pass_time
            blog.info(f'用时: {pass_time}')

            # 删除多余的日志
            try:
                if logfile:
                    logfile_list = list(logfile.parent.glob('*.log'))
                    logfile_list.remove(logfile)
                    logfile_list.sort()
                    logfile_list = logfile_list[_LOGFILE_COUNT:]
                    await bpath.remove(*logfile_list)
            except:
                pass


def _get_root_dir():
    frametype = inspect.currentframe()
    target = frametype
    while True:
        assert target and target.f_back
        target = target.f_back
        if target.f_locals.get('__name__') == '__main__':
            file = target.f_locals.get('__file__')
            if type(file) is str:
                return bpath.get(file).parent


def _check_vscode_venv():
    par = '--vscode-venv'
    if par in sys.argv:
        sys.argv.remove(par)
        sys.orig_argv.remove(par)
        input('回车后继续（为了兼容vscode venv问题）...')
