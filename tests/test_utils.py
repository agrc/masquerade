from unittest.mock import MagicMock

from masquerade.utils import cleanse_text, get_out_spatial_reference


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
