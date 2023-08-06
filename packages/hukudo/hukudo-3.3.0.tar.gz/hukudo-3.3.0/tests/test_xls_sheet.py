import pytest

from hukudo.xls import TableError, fmt
from hukudo.xls.sheet import Sheet


def test_add_table(sh, table):
    sh.add_table('B2', table)


def test_add_table_top_down(sh, table_single_row):
    sh.add_table_top_down('A1', table_single_row)


def test_add_table_top_down_error(sh, table):
    with pytest.raises(TableError):
        sh.add_table_top_down('A1', table)


def test_add_table_with_header(wb, table):
    # add the style "h2"
    wb.add_named_style(fmt.h2)
    sh = Sheet(wb.active)
    sh.add_table_with_header('A1', 'my table header', table, fmt.h2.name)


def test_fill_row(sh):
    sh.fill_row('A1', 'Z', fmt.h1.fill)


def test_auto_set_column_width(sh):
    sh.auto_set_column_width()
