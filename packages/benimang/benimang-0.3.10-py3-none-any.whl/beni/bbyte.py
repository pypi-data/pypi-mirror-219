import struct
from typing import Any, Literal

from beni import bfunc


def decode(value: bytes):
    import chardet
    data = chardet.detect(value)
    encoding = data['encoding'] or 'utf8'
    return value.decode(encoding)


EndianType = Literal[
    # https://docs.python.org/zh-cn/3/library/struct.html#byte-order-size-and-alignment
    '@',  # 按原字节
    '=',  # 按原字节
    '<',  # 小端
    '>',  # 大端
    '!',  # 网络（=大端）
]


class BytesWriter():

    def __init__(self, endian: EndianType):
        self.endian = endian
        self.fmt_ary: list[str] = []
        self.data_ary: list[Any] = []

    def to_bytes(self):
        return struct.pack(
            f'{self.endian}{"".join(self.fmt_ary)}',
            *self.data_ary
        )

    def _write(self, fmt: str, data: int | float | bool | str | bytes):
        self.fmt_ary.append(fmt)
        self.data_ary.append(data)

    def _write_ary(self, func: Any, ary: list[Any]):
        self.uint32(len(ary))
        for value in ary:
            func(value)
        return self

    def int16(self, data: int):
        '''short'''
        self._write('h', bfunc.get_inside(data, -32768, 32767))  # int16
        return self

    def uint16(self, data: int):
        '''unsigned short'''
        self._write('H', bfunc.get_inside(data, 0, 65535))  # int16
        return self

    def int32(self, data: int):
        '''int'''
        self._write('i', bfunc.get_inside(data, -2147483648, 2147483647))  # int32
        return self

    def uint32(self, data: int):
        '''unsigned int'''
        self._write('I', bfunc.get_inside(data, 0, 4294967295))  # int32
        return self

    def int64(self, data: int):
        '''long long'''
        self._write('q', bfunc.get_inside(data, -9223372036854775808, 9223372036854775807))  # int64
        return self

    def uint64(self, data: int):
        '''unsigned long long'''
        self._write('Q', bfunc.get_inside(data, 0, 18446744073709551615))  # int64
        return self

    def float32(self, data: float):
        '''float'''
        self._write('f', data)
        return self

    def float64(self, data: float):
        '''double'''
        self._write('d', data)
        return self

    def boolean(self, data: bool):
        self._write('?', data)
        return self

    def string(self, data: str):
        data_bytes = data.encode('utf8')
        num = len(data_bytes)
        self.uint16(num)
        self._write(f'{num}s', data_bytes)
        return self

    def int16_ary(self, ary: list[int]):
        '''short array'''
        return self._write_ary(self.int16, ary)

    def uint16_ary(self, ary: list[int]):
        '''unsigned short array'''
        return self._write_ary(self.uint16, ary)

    def int32_ary(self, ary: list[int]):
        '''int array'''
        return self._write_ary(self.int32, ary)

    def uint32_ary(self, ary: list[int]):
        '''unsigned int array'''
        return self._write_ary(self.uint32, ary)

    def int64_ary(self, ary: list[int]):
        '''long long array'''
        return self._write_ary(self.int64, ary)

    def uint64_ary(self, ary: list[int]):
        '''unsigned long long array'''
        return self._write_ary(self.uint64, ary)

    def float32_ary(self, ary: list[float]):
        '''float array'''
        return self._write_ary(self.float32, ary)

    def float64_ary(self, ary: list[float]):
        '''double array'''
        return self._write_ary(self.float64, ary)

    def boolean_ary(self, ary: list[bool]):
        return self._write_ary(self.boolean, ary)

    def string_ary(self, ary: list[str]):
        return self._write_ary(self.string, ary)


class BytesReader():

    def __init__(self, endian: EndianType, data: bytes):
        self.endian = endian
        self.offset: int = 0
        self.data: bytes = data

    def _read(self, fmt: str):
        result = struct.unpack_from(fmt, self.data, self.offset)[0]
        self.offset += struct.calcsize(fmt)
        return result

    def _read_ary(self, func: Any):
        ary: list[Any] = []
        num = self.uint32()
        for _ in range(num):
            ary.append(func())
        return ary

    def int16(self) -> int:
        '''short'''
        return self._read('h')

    def uint16(self) -> int:
        '''unsigned short'''
        return self._read('H')

    def int32(self) -> int:
        '''int'''
        return self._read('i')

    def uint32(self) -> int:
        '''unsigned int'''
        return self._read('I')

    def int64(self) -> int:
        '''long long'''
        return self._read('q')

    def uint64(self) -> int:
        '''unsigned long long'''
        return self._read('Q')

    def float32(self) -> float:
        '''float'''
        return self._read('f')

    def float64(self) -> float:
        '''double'''
        return self._read('d')

    def boolean(self) -> bool:
        return self._read('?')

    def string(self) -> str:
        num = self.uint16()
        return self._read(f'{num}s').decode()

    def int16_ary(self) -> list[int]:
        '''short array'''
        return self._read_ary(self.int16)

    def uint16_ary(self) -> list[int]:
        '''unsigned short array'''
        return self._read_ary(self.uint16)

    def int32_ary(self) -> list[int]:
        '''int array'''
        return self._read_ary(self.int32)

    def uint32_ary(self) -> list[int]:
        '''unsigned int array'''
        return self._read_ary(self.uint32)

    def int64_ary(self) -> list[int]:
        '''long long array'''
        return self._read_ary(self.int64)

    def uint64_ary(self) -> list[int]:
        '''unsigned long long array'''
        return self._read_ary(self.uint64)

    def float32_ary(self) -> list[float]:
        '''float array'''
        return self._read_ary(self.float32)

    def float64_ary(self) -> list[float]:
        '''double array'''
        return self._read_ary(self.float64)

    def boolean_ary(self) -> list[bool]:
        return self._read_ary(self.boolean)

    def string_ary(self) -> list[str]:
        return self._read_ary(self.string)
