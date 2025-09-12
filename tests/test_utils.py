from unittest.mock import MagicMock

from markupsafe import Markup

from masquerade.utils import cleanse_text, escape_while_preserving_numbers, get_out_spatial_reference


def test_removes_spaces():
    assert cleanse_text("  hello  ") == "hello"


def test_removes_quotes():
    assert cleanse_text('"hello"') == "hello"
    assert cleanse_text("test 'hello") == "test hello"


def test_cleanse_text_without_strings():
    assert cleanse_text(None) is None
    assert cleanse_text(1) == 1
    assert cleanse_text({}) == {}


def test_get_out_spatial_reference_get_request():
    request = MagicMock()
    request.method = "GET"
    request.args = {"outSR": 3857}

    assert get_out_spatial_reference(request) == (3857, 3857)


def test_get_out_spatial_reference_get_request_json():
    request = MagicMock()
    request.method = "GET"
    request.args = {"outSR": '{"wkid": 3857}'}

    assert get_out_spatial_reference(request) == (3857, 3857)


def test_get_out_spatial_reference_default():
    request = MagicMock()
    request.method = "GET"
    request.args = {}
    request.form = {}

    assert get_out_spatial_reference(request) == (4326, 4326)


def test_get_out_spatial_reference_post_request():
    request = MagicMock()
    request.method = "POST"
    request.form = {"outSR": 3857}

    assert get_out_spatial_reference(request) == (3857, 3857)


def test_escape_while_preserving_numbers_with_int():
    assert escape_while_preserving_numbers(123) == 123


def test_escape_while_preserving_numbers_with_float():
    assert escape_while_preserving_numbers(123.45) == 123.45


def test_escape_while_preserving_numbers_with_string():
    assert escape_while_preserving_numbers("<script>") == Markup("&lt;script&gt;")


def test_escape_while_preserving_numbers_with_safe_string():
    assert escape_while_preserving_numbers(Markup("<strong>safe</strong>")) == Markup("<strong>safe</strong>")


def test_text_is_empty():
    from masquerade.utils import text_is_empty

    assert text_is_empty(None) is True
    assert text_is_empty("") is True
    assert text_is_empty("   ") is True
    assert text_is_empty("text") is False
    assert text_is_empty("  text  ") is False
