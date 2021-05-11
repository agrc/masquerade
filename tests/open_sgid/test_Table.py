#!/usr/bin/env python
# * coding: utf8 *
"""
A module that contains tests for the open_sgid.Table class
"""

import re
from unittest import mock

from callee import Contains

from masquerade.providers.open_sgid import POINT, POLYGON, Table, normalize_prefix_direction

table = Table('table_name', 'name', POLYGON)


@mock.patch('masquerade.providers.open_sgid.database')
def test_get_suggestions(database_mock):
    mocked_results = [[1, 'search text'], [2, 'more search text']]
    database_mock.query.return_value = mocked_results

    suggestions = table.get_suggestions('blah', 10)

    assert len(suggestions) == 2
    database_mock.query.assert_called_with(Contains('ilike \'blah%\''))


@mock.patch('masquerade.providers.open_sgid.database')
def test_get_candidate_from_magic_key(database_mock):
    mocked_result = [[1, 'match text', 1, 2, 3, 4, 5, 6]]

    database_mock.query.return_value = mocked_result

    candidate = table.get_candidate_from_magic_key(1, 3857)

    assert candidate['text'] == 'match text'
    assert candidate['attributes']['Score'] == 100
    assert candidate['location']['x'] == 1
    assert candidate['location']['y'] == 2
    assert candidate['extent']['xmax'] == 3
    assert candidate['extent']['ymax'] == 4
    assert candidate['extent']['xmin'] == 5
    assert candidate['extent']['ymin'] == 6


def test_get_magic_key_query():
    point_table = Table('point_table_name', 'name', POINT)

    point_query = point_table.get_magic_key_query(1, 1234)

    #: manually expandes extent
    assert re.search('st_expand', point_query)

    polygon_table = Table('point_table_name', 'name', POLYGON)

    polygon_table = polygon_table.get_magic_key_query(1, 1234)

    #: manually expandes extent
    assert re.search('st_expand', polygon_table) is None


def test_get_suggestion_from_record_with_context():
    suggestion = table.get_suggestion_from_record(1, 'match text', 'context value', 'another value')

    assert suggestion['text'] == 'match text, context value, another value'


def test_address_points_normalizes_first_direction_in_suggestions():
    tests = [
        ('1234 North 1234 East', '1234 n 1234 east'),
        ('1234 No 1234 East', '1234 n 1234 east'),
        ('1234 So', '1234 s'),
        ('1235 Eas hello', '1235 e hello'),
        ('1235 E. hello', '1235 e hello'),
        ('1235 Ea. hello', '1235 e hello'),
        ('1234', '1234'),
    ]
    for input, expected in tests:
        text = normalize_prefix_direction(input)

        assert text == expected
