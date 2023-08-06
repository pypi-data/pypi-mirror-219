from __future__ import annotations

import typing
from typing import Union

from openpyxl import utils as openpyxl_utils
from openpyxl.utils.cell import coordinate_from_string


class EDI(str):
    """
    Excel Document Iterator
    """

    def __new__(cls, coords):
        return super().__new__(cls, coords)

    def __repr__(self):
        return f"'{self.col}{self.row}'"

    @classmethod
    def from_col_row(cls, col: str, row: int):
        return cls(f'{col}{row}')

    @property
    def tuple(self) -> tuple[str, int]:
        """
        >>> EDI('B4').tuple
        ('B', 4)
        """
        return coordinate_from_string(self)

    @property
    def col(self):
        return self.tuple[0]

    @property
    def row(self):
        return self.tuple[1]

    @property
    def col_num(self):
        """
        >>> EDI('B4').col_num
        2
        """
        return openpyxl_utils.column_index_from_string(self.col)

    def at_row(self, i) -> EDI:
        return self.__class__(f'{self.col}{i}')

    def at_col(self, col):
        """
        >>> EDI('B23').at_col('A')
        'A23'
        """
        return self.from_col_row(col, self.row)

    def row_offset(self, i) -> EDI:
        """
        >>> EDI('B4').row_offset(2)
        'B6'
        """
        return self.at_row(self.row + i)

    def col_offset(self, i: int) -> EDI:
        """
        >>> EDI('B4').col_offset(2)
        'D4'
        """
        return self.at_col(openpyxl_utils.get_column_letter(self.col_num + i))

    def with_row_indices(self, values: typing.Iterable[str]) -> dict:
        """
        >>> EDI('B4').with_row_indices(['foo', 'bar', 'baz'])
        {'B4': 'foo', 'B5': 'bar', 'B6': 'baz'}
        """
        result = {}
        for i, value in enumerate(values):
            result[self.row_offset(i)] = value
        return result

    def with_col_indices(self, values: typing.Iterable[str]) -> dict:
        """
        >>> EDI('B4').with_col_indices(['foo', 'bar', 'baz'])
        {'B4': 'foo', 'C4': 'bar', 'D4': 'baz'}
        """
        result = {}
        for i, value in enumerate(values):
            result[self.col_offset(i)] = value
        return result

    def get_range_col_offset(self, i: int):
        """
        >>> EDI('B4').get_range_col_offset(2)
        'B4:D4'
        """
        return f'{self}:{self.col_offset(i)}'


EDISTR = Union[EDI, str]
