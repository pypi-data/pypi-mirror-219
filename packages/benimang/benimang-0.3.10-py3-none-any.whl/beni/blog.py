import asyncio
import logging
import re
from pathlib import Path
from typing import Any

from colorama import Fore

from beni import bcolor, bpath

_name = 'beni'

_warning_count = 0
_error_count = 0
_critical_count = 0


def init(name: str = '', level: int = logging.INFO, file: Path | None = None):
    FORMAT = '%(asctime)s %(levelname)-1s %(message)s', '%Y-%m-%d %H:%M:%S'
    LEVEL_NAME = {
        logging.DEBUG: 'D',
        logging.INFO: '',
        logging.WARNING: 'W',
        logging.ERROR: 'E',
        logging.CRITICAL: 'C',
    }

    if name:
        global _name
        _name = name

    logger = logging.getLogger(_name)
    logger.setLevel(level)
    for k, v in LEVEL_NAME.items():
        logging.addLevelName(k, v)

    formatter = logging.Formatter(*FORMAT)

    class CustomStreamHandler(logging.StreamHandler):  # type: ignore

        def emit(self, record: logging.LogRecord):
            try:
                msg = self.format(record) + self.terminator
                # issue 35046: merged two stream.writes into one.
                func = self.stream.write
                if record.levelno == logging.WARNING:
                    global _warning_count
                    _warning_count += 1
                    bcolor.set_colors(Fore.YELLOW)
                elif record.levelno == logging.ERROR:
                    global _error_count
                    _error_count += 1
                    bcolor.set_colors(Fore.LIGHTRED_EX)
                elif record.levelno == logging.CRITICAL:
                    global _critical_count
                    _critical_count += 1
                    bcolor.set_colors(Fore.LIGHTMAGENTA_EX)
                func(msg)
                bcolor.reset_colors()
                self.flush()
            except RecursionError:  # See issue 36272
                raise
            except Exception:
                self.handleError(record)

    handler = CustomStreamHandler()
    handler.setFormatter(formatter)
    handler.setLevel(level)
    logger.addHandler(handler)

    if file:

        class CustomFileHandler(logging.FileHandler):

            _write_func: Any
            _xx = re.compile(r'\x1b\[\d+m')

            def _open(self):
                result = super()._open()
                self._write_func = result.write
                setattr(result, 'write', self._write)
                return result

            def _write(self, msg: str):
                msg = self._xx.sub('', msg)
                self._write_func(msg)

        asyncio.run(bpath.make(file.parent))
        file_handler = CustomFileHandler(file, delay=True)
        file_handler.setFormatter(formatter)
        file_handler.setLevel(level)
        logger.addHandler(file_handler)


def debug(msg: Any, wrap: bool = False, *args: Any, **kwargs: Any):
    logging.getLogger(_name).debug(_format(msg, wrap), *args, **kwargs)


def info(msg: Any, wrap: bool = False, *args: Any, **kwargs: Any):
    logging.getLogger(_name).info(_format(msg, wrap), *args, **kwargs)


def warning(msg: Any, wrap: bool = False, *args: Any, **kwargs: Any):
    logging.getLogger(_name).warning(_format(msg, wrap), *args, **kwargs)


def error(msg: Any, wrap: bool = False, *args: Any, **kwargs: Any):
    logging.getLogger(_name).error(_format(msg, wrap), *args, **kwargs)


def critical(msg: Any, wrap: bool = False, *args: Any, **kwargs: Any):
    logging.getLogger(_name).critical(_format(msg, wrap), *args, **kwargs)


def _format(msg: Any, wrap: bool):
    if wrap:
        return '\n\n' + msg + '\n'
    else:
        return msg


def get_warning_count():
    return _warning_count


def set_warning_count(value: int):
    global _warning_count
    _warning_count = value


def get_error_count():
    return _error_count


def set_error_count(value: int):
    global _error_count
    _error_count = value


def get_critical_count():
    return _critical_count


def set_critical_count(value: int):
    global _critical_count
    _critical_count = value
