#!/usr/bin/env python
# * coding: utf8 *
"""
A module that contains tests for open_sgid.
"""

from unittest import mock

from pytest import raises

from masquerade.providers.open_sgid import (
    POINT,
    FullTextTable,
    NoTableFoundException,
    get_boundary_value,
    get_candidate_from_magic_key,
    get_suggestions,
    get_table_from_table_name,
)


def test_get_suggestions():
    mock1 = mock.Mock()
    mock1.get_suggestions.return_value = [1, 2]
    mock2 = mock.Mock()
    mock2.get_suggestions.return_value = [3]

    with mock.patch("masquerade.providers.open_sgid.TABLES", new=[mock1, mock2]):
        suggestions = get_suggestions("hello", 10)

    assert suggestions == [1, 2, 3]


def test_get_candidate_from_magic_key():
    mock1 = mock.Mock()
    mock1.table_name = "name1"
    mock1.get_candidate_from_magic_key.return_value = 1
    mock2 = mock.Mock()
    mock2.table_name = "name2"

    with mock.patch("masquerade.providers.open_sgid.TABLES", new=[mock1, mock2]):
        assert get_candidate_from_magic_key("1-name1", 1234) == 1


def test_get_table_from_table_name():
    mock1 = mock.Mock()
    mock1.table_name = "name1"
    mock2 = mock.Mock()
    mock2.table_name = "name2"

    with mock.patch("masquerade.providers.open_sgid.TABLES", new=[mock1, mock2]):
        with raises(NoTableFoundException, match="No table found"):
            get_table_from_table_name("blah")


def test_full_text_table():
    table = FullTextTable("table_name", "search_field", POINT)

    assert "%hello%" in table.get_suggest_query("hello", 10)


def test_get_boundary_value():
    mock_db = mock.Mock()
    mock_db.query.return_value = [("boundary_value",)]

    with mock.patch("masquerade.providers.open_sgid.database", new=mock_db):
        value = get_boundary_value(1, 2, 4326, "table_name", "field_name")
        assert value == "boundary_value"

    mock_db.query.return_value = []

    with mock.patch("masquerade.providers.open_sgid.database", new=mock_db):
        value = get_boundary_value(1, 2, 4326, "table_name", "field_name")
        assert value is None
