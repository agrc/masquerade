#!/usr/bin/env python
# * coding: utf8 *
"""
A module that contains tests for the open_sgid.Table class
"""

import re
from unittest import mock

from callee import Contains

from masquerade.providers.open_sgid import POINT, POLYGON, Table

table = Table('table_name', 'name', [], POLYGON)


@mock.patch('masquerade.providers.open_sgid.connection')
def test_get_suggestions(connect_mock):
    mocked_results = [[1, 'search text'], [2, 'more search text']]
    cursor_mock = connect_mock.cursor.return_value
    cursor_mock.fetchall.return_value = mocked_results

    suggestions = table.get_suggestions('blah', 10)

    assert len(suggestions) == 2
    cursor_mock.execute.assert_called_with(Contains('ilike \'blah%\''))


@mock.patch('masquerade.providers.open_sgid.connection')
def test_get_candidate_from_magic_key(connect_mock):
    mocked_result = [1, 'match text', 1, 2, 3, 4, 5, 6]

    cursor_mock = connect_mock.cursor.return_value
    cursor_mock.fetchone.return_value = mocked_result

    candidate = table.get_candidate_from_magic_key(1, 3857)

    assert candidate['text'] == 'match text'
    assert candidate['attributes']['score'] == 100
    assert candidate['location']['x'] == 1
    assert candidate['location']['y'] == 2
    assert candidate['extent']['xmax'] == 3
    assert candidate['extent']['ymax'] == 4
    assert candidate['extent']['xmin'] == 5
    assert candidate['extent']['ymin'] == 6


def test_get_magic_key_query():
    point_table = Table('point_table_name', 'name', [], POINT)

    point_query = point_table.get_magic_key_query(1, 1234)

    #: manually expandes extent
    assert re.search('st_expand', point_query)

    polygon_table = Table('point_table_name', 'name', [], POLYGON)

    polygon_table = polygon_table.get_magic_key_query(1, 1234)

    #: manually expandes extent
    assert re.search('st_expand', polygon_table) is None


def test_get_suggestion_from_record_with_context():
    suggestion = table.get_suggestion_from_record(1, 'match text', 'context value')

    assert suggestion['text'] == 'match text, context value'
