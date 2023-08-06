import getpass
import random
from dataclasses import dataclass
from types import FunctionType
from typing import Any, Callable, Coroutine, cast

from beni import bcolor


async def hold(msg: str | None = None, password: bool = False, *exits: str):
    msg = msg or '测试暂停，输入exit可以退出'
    msg = f'{msg}: '
    exits = exits or ('exit',)
    while True:
        if password:
            value = getpass.getpass(msg)
        else:
            import aioconsole
            value = cast(str, await aioconsole.ainput(msg))
        if (value in exits) or ('*' in exits):
            return value


async def confirm(msg: str = '确认', show_input: bool = False):
    '输入验证码继续（随机3位数字的验证码）'
    code = f'{random.randint(1, 999):03}'
    await hold(f'{msg} [ {bcolor.get_yellow(code)} ]', not show_input, code)


@dataclass
class Selections:
    msg: str
    desc: str | None = None
    confirm: str | Callable[[str], Any] | None = None
    handler: Callable[[str], Coroutine[Any, Any, Any]] | None = None


async def select(*data_ary: Selections):
    '''
    async def main():
        value = await binput.select(
            binput.Selections('msgA', 'descA', 'confirmTextA', __handlerA),
            binput.Selections('msgB', 'descB', 'confirmTextB', __handlerB),
        )
        print(value)

    async def __handlerA(value: str):
        print('run __handlerA')

    async def __handlerB(value: str):
        print('run __handlerB')
    '''
    print()
    print('-' * 30)
    print()
    for item in data_ary:
        if item.desc:
            print(f'{item.msg} [ {bcolor.get_yellow(item.desc)} ]')
        else:
            print(item.msg)
    print()
    import aioconsole
    while True:
        value = cast(str, await aioconsole.ainput('输入选择：'))
        isMatch = False
        for item in data_ary:
            check = item.confirm or item.desc or item.msg
            if type(check) is str:
                isMatch = value == check
            elif type(check) is FunctionType:
                try:
                    isMatch = check(value)
                except:
                    pass
            if isMatch:
                if item.handler:
                    await item.handler(value)
                return value


async def input_check(msg: str, check_func: Callable[[str], Any]):
    import aioconsole
    while True:
        try:
            value = cast(str, await aioconsole.ainput(f'{msg}：'))
            if check_func(value):
                return value
        except:
            pass
