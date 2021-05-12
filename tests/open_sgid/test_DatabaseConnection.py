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
    Cursor = namedtuple('Cursor', ['execute', 'fetchall'])
    cursor_mock = Cursor(lambda _: None, lambda: expected_data)
    Connection = namedtuple('Connection', ['cursor', 'closed'])
    open_connection = Connection(lambda: cursor_mock, 0)
    closed_connection = Connection(lambda: cursor_mock, 1)
    psycopg_mock.connect.side_effect = [open_connection, closed_connection]

    database = DatabaseConnection()

    database.query('blah')
    result = database.query('query text')

    assert result == expected_data
    assert psycopg_mock.connect.call_count == 1


@mock.patch('masquerade.providers.open_sgid.psycopg2')
def test_get_magic_key_record(psycopg_mock):
    expected_data = ['blah']
    Cursor = namedtuple('Cursor', ['execute', 'fetchone', 'description'])
    cursor_mock = Cursor(
        lambda _: None, lambda: expected_data,
        ['xid', 'search_field', 'x', 'y', 'xmin', 'xmax', 'ymin', 'ymax', 'another_field', 'shape']
    )
    Connection = namedtuple('Connection', ['cursor', 'closed'])
    open_connection = Connection(lambda: cursor_mock, 0)
    closed_connection = Connection(lambda: cursor_mock, 1)
    psycopg_mock.connect.side_effect = [open_connection, closed_connection]

    database = DatabaseConnection()

    record, field_names = database.get_magic_key_record('query text')

    assert record[0] == 'blah'

    #: should filter out shape value
    assert not 'shape' in field_names
