from masquerade.utils import cleanse_text


def test_removes_spaces():
    assert cleanse_text('  hello  ') == 'hello'


def test_removes_quotes():
    assert cleanse_text('"hello"') == 'hello'
    assert cleanse_text('test \'hello') == 'test hello'
