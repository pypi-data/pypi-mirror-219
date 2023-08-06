import sys
from typing import IO, Any

from colorama import Fore, Style, init

_inited = False

if not _inited:
    _inited = True
    init()


def printx(*values: Any, sep: str = ' ', end: str = '\n', file: IO[str] = sys.stdout, flush: bool = False, colors: list[Any] | None):
    '''color 数组参数 colorama.Fore / colorama.Back / colorama.Style 的常量'''
    if colors:
        set_colors(*colors)
    print(*values, sep=sep, end=end, file=file, flush=flush)
    reset_colors()


def get_str(value: Any, *colors: Any):
    if colors:
        value = ''.join(colors) + str(value) + Style.RESET_ALL
    return value


def set_colors(*colors: Any):
    content = ''.join(colors)
    if content:
        sys.stdout.write(content)
        sys.stderr.write(content)


def reset_colors():
    sys.stdout.write(Style.RESET_ALL)
    sys.stderr.write(Style.RESET_ALL)


def get_red(msg: str):
    return get_str(msg, Fore.LIGHTRED_EX)


def get_yellow(msg: str):
    return get_str(msg, Fore.YELLOW)


def get_green(msg: str):
    return get_str(msg, Fore.LIGHTGREEN_EX)


def get_cyan(msg: str):
    '蓝色'
    return get_str(msg, Fore.LIGHTCYAN_EX)


def get_magenta(msg: str):
    '紫色'
    return get_str(msg, Fore.LIGHTMAGENTA_EX)


def get_white(msg: str):
    return get_str(msg, Fore.LIGHTWHITE_EX)


def print_red(*msgs: Any):
    print(get_red(' '.join([str(x) for x in msgs])))


def print_yellow(*msgs: Any):
    print(get_yellow(' '.join([str(x) for x in msgs])))


def print_green(*msgs: Any):
    print(get_green(' '.join([str(x) for x in msgs])))


def print_cyan(*msgs: Any):
    '蓝色'
    print(get_cyan(' '.join([str(x) for x in msgs])))


def print_magenta(*msgs: Any):
    '紫色'
    print(get_magenta(' '.join([str(x) for x in msgs])))


def print_white(*msgs: Any):
    print(get_white(' '.join([str(x) for x in msgs])))
