def test_change_columns(ws, table):
    # drop second column and rename last column
    table.change_columns(
        {
            'col2': None,
            'col3': 'Column Three',
        }
    )
    # note that change_columns automatically capitalizes column names
    assert table.header == ['Col1', 'Column Three', 'ID']
    assert table.data == [
        ['first', 'data', 'id data'],
        ['second', 'data', 'id data'],
    ]
