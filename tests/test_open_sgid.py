#!/usr/bin/env python
# * coding: utf8 *
"""
A module that contains tests for open_sgid.
"""

from unittest import mock

from callee import Contains

from masquerade.providers.open_sgid import (
    connection, get_candidate_from_magic_key, get_suggestion_from_record, get_suggestions
)


def test_get_suggestion_from_record_with_city():
    suggestion = get_suggestion_from_record(1, 'full_add', 'address_system', 'city')

    assert suggestion['isCollection'] == False
    assert suggestion['magicKey'] == 1
    assert suggestion['text'] == 'full_add, city'


def test_get_suggestion_from_record_without_city():
    suggestion = get_suggestion_from_record(1, 'full_add', 'address_system', None)

    assert suggestion['isCollection'] == False
    assert suggestion['magicKey'] == 1
    assert suggestion['text'] == 'full_add, address_system'


@mock.patch('masquerade.providers.open_sgid.connection')
def test_get_suggestions(connect_mock):
    mocked_results = [[1, 'fulladd', 'some address system', 'some city'],
                      [2, 'another full add', 'another add sys', 'city']]
    cursor_mock = connect_mock.cursor.return_value
    cursor_mock.fetchall.return_value = mocked_results

    suggestions = get_suggestions('blah')

    assert len(suggestions) == 2
    cursor_mock.execute.assert_called_with(Contains('like upper(\'blah%\')'))


@mock.patch('masquerade.providers.open_sgid.connection')
def test_get_candidate_from_magic_key(connect_mock):
    mocked_result = [1, 'fulladd', 'some address system', 'some city', 2, 3]

    cursor_mock = connect_mock.cursor.return_value
    cursor_mock.fetchone.return_value = mocked_result

    candidate = get_candidate_from_magic_key(1, 3857)

    assert candidate['address'] == 'fulladd, some city'
    assert candidate['attributes']['score'] == 100
    assert candidate['location']['x'] == 2
    assert candidate['location']['y'] == 3
