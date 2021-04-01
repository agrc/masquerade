#!/usr/bin/env python
# * coding: utf8 *
"""
A module that contains tests for the open_sgid.DatabaseConnection class
"""

from collections import namedtuple
from typing import NamedTuple
from unittest import mock

from masquerade.providers.open_sgid import DatabaseConnection


@mock.patch('masquerade.providers.open_sgid.psycopg2')
def test_query(psycopg_mock):
    expected_data = ['blah']
    Cursor = namedtuple('Cursor', ['execute', 'fetchall'])
    cursor_mock = Cursor(lambda _: None, lambda: expected_data)
    Connection = namedtuple('Connection', ['cursor', 'closed'])
    psycopg_mock.connect.return_value = Connection(lambda: cursor_mock, False)

    database = DatabaseConnection()

    result = database.query('query text')

    assert result == expected_data
