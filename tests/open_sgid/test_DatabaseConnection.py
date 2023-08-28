#!/usr/bin/env python
# * coding: utf8 *
"""
A module that contains tests for the open_sgid.DatabaseConnection class
"""

from unittest import mock

from masquerade.providers.open_sgid import DatabaseConnection


@mock.patch("masquerade.providers.open_sgid.pool")
def test_query(pool_mock):
    expected_data = ["blah"]

    cursor = mock.MagicMock()
    cursor.fetchall.return_value = expected_data
    cursor_func = mock.MagicMock()
    cursor_func.__enter__ = mock.MagicMock(return_value=cursor)
    connection = mock.MagicMock()
    connection.cursor.return_value = cursor_func
    connection_func = mock.MagicMock()
    connection_func.__enter__ = mock.MagicMock(return_value=connection)
    pool_mock.connection = mock.MagicMock(return_value=connection_func)

    database = DatabaseConnection()

    database.query("blah")
    result = database.query("query text")

    assert result == expected_data


@mock.patch("masquerade.providers.open_sgid.pool")
def test_get_magic_key_record(pool_mock):
    expected_data = ["blah"]
    description = [
        "xid",
        "search_field",
        "x",
        "y",
        "xmin",
        "xmax",
        "ymin",
        "ymax",
        "another_field",
        "shape",
    ]
    cursor = mock.MagicMock()
    cursor.fetchone.return_value = expected_data
    cursor.description = description
    cursor_func = mock.MagicMock()
    cursor_func.__enter__ = mock.MagicMock(return_value=cursor)
    connection = mock.MagicMock()
    connection.cursor.return_value = cursor_func
    connection_func = mock.MagicMock()
    connection_func.__enter__ = mock.MagicMock(return_value=connection)
    pool_mock.connection = mock.MagicMock(return_value=connection_func)

    database = DatabaseConnection()

    record, field_names = database.get_magic_key_record("query text")

    assert record[0] == "blah"

    #: should filter out shape value
    assert "shape" not in field_names
