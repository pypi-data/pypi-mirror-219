from typing import Any, Callable, Sequence, Tuple

import colorama

from beni import bcolor
from beni.btype import AnyType


def get(
    data_list: Sequence[AnyType],
    *,
    title: str | None = None,
    fields: Sequence[Tuple[str, Callable[[AnyType], Any]]],
    rowcolor: Callable[[list[Any]], Any] | None = None,
    extend: list[list[Any]] | None = None,
    isPrint: bool = False,
):
    HEADER_COLOR = colorama.Fore.YELLOW
    from prettytable import PrettyTable
    table = PrettyTable()
    if title:
        table.title = bcolor.get_str(title, HEADER_COLOR)
    field_funclist: list[Callable[[AnyType], Any]] = []
    field_namelist: list[str] = []
    align_dict: dict[str, str] = {}
    for i in range(len(fields)):
        item = fields[i]
        field_funclist.append(item[1])
        field_name = item[0]
        if field_name.endswith('>'):
            field_name = field_name[:-1]
            align_dict[field_name] = 'r'
        elif field_name.endswith('<'):
            field_name = field_name[:-1]
            align_dict[field_name] = 'l'
        field_namelist.append(field_name)
    table.field_names = [bcolor.get_str(x, HEADER_COLOR) for x in field_namelist]
    for k, v in align_dict.items():
        table.align[bcolor.get_str(k, HEADER_COLOR)] = v
    row_list: list[list[Any]] = []
    for data in data_list:
        row = [func(data) for func in field_funclist]
        row_list.append(row)
    if extend:
        for row in extend:
            newRow = row[:]
            if len(newRow) < len(fields):
                newRow.extend([''] * (len(fields) - len(newRow)))
            row_list.append(newRow)
    if rowcolor:
        for row in row_list:
            color = rowcolor(row)
            if color:
                for i in range(len(row)):
                    row[i] = bcolor.get_str(row[i], color)
    table.add_rows(row_list)
    tableStr = str(table.get_string())
    if isPrint:
        print(f'\n{tableStr}\n')
    return tableStr
