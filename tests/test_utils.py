from masquerade.utils import cleanse_text


def test_removes_spaces():
    assert cleanse_text("  hello  ") == "hello"


def test_removes_quotes():
    assert cleanse_text('"hello"') == "hello"
    assert cleanse_text("test 'hello") == "test hello"


def test_cleanse_text_without_strings():
    assert cleanse_text(None) is None
    assert cleanse_text(1) == 1
    assert cleanse_text({}) == {}
