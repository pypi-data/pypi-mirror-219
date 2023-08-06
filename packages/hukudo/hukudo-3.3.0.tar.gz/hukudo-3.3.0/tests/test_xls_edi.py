from hukudo.xls.edi import EDI


def test_simple(ws):
    edi = EDI('B4')
    assert repr(edi) == "'B4'"
    ws[edi] = 'Hello'
