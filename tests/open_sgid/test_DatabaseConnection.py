#!/usr/bin/env python
# * coding: utf8 *
"""
A module that contains tests for the open_sgid.DatabaseConnection class
"""

from collections import namedtuple
from unittest import mock

from masquerade.providers.open_sgid import DatabaseConnection


@mock.patch('masquerade.providers.open_sgid.psycopg2')
def test_query(psycopg_mock):
    expected_data = ['blah']
    open_connection = mock.MagicMock()
    open_connection.closed = 0
    with open_connection.cursor() as cursor_mock:
        cursor_mock.fetchall.return_value = expected_data

    closed_connection = mock.MagicMock()
    closed_connection.closed = 1
    psycopg_mock.connect.side_effect = [open_connection, closed_connection]

    database = DatabaseConnection()

    database.query('blah')
    result = database.query('query text')

    assert result == expected_data
    assert psycopg_mock.connect.call_count == 1


@mock.patch('masquerade.providers.open_sgid.psycopg2')
def test_get_magic_key_record(psycopg_mock):
    expected_data = ['blah']
    description = ['xid', 'search_field', 'x', 'y', 'xmin', 'xmax', 'ymin', 'ymax', 'another_field', 'shape']
    open_connection = mock.MagicMock()
    open_connection.closed = 0
    with open_connection.cursor() as cursor_mock:
        cursor_mock.fetchone.return_value = expected_data
        cursor_mock.description = description

    closed_connection = mock.MagicMock()
    closed_connection.closed = 1
    psycopg_mock.connect.side_effect = [open_connection, closed_connection]

    database = DatabaseConnection()

    record, field_names = database.get_magic_key_record('query text')

    assert record[0] == 'blah'

    #: should filter out shape value
    assert not 'shape' in field_names
