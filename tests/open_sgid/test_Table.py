#!/usr/bin/env python
# * coding: utf8 *
"""
A module that contains tests for the open_sgid.Table class
"""

import re
from unittest import mock

from callee import Contains
from pytest import raises

from masquerade.providers.open_sgid import (
    NUMERIC,
    POINT,
    POLYGON,
    Table,
    normalize_prefix_direction,
)

table = Table("table_name", "name", POLYGON)


def test_get_suggest_query_text():
    text_table = Table("text_table_name", "name", POINT)

    text_query = text_table.get_suggest_query("match text", 1)

    assert "'match text%'" in text_query


def test_get_suggest_query_number():
    text_table = Table("text_table_name", "name", POINT, NUMERIC)

    text_query = text_table.get_suggest_query("9", 1)

    assert "name = 9" in text_query

    with raises(ValueError):
        text_table.get_suggest_query("text", 1)


def test_get_suggest_query_search_key():
    table = Table(
        "table_name",
        "name",
        POLYGON,
        search_field_type=NUMERIC,
        search_key="search_key",
    )

    query = table.get_suggest_query("1 search_key", 1)

    assert "name = 1" in query

    partial_query = table.get_suggest_query("1 sear", 1)

    assert "name = 1" in partial_query

    with raises(ValueError):
        table.get_suggest_query("1 blah", 1)


@mock.patch("masquerade.providers.open_sgid.database")
def test_get_suggestions(database_mock):
    mocked_results = [[1, "search text"], [2, "more search text"]]
    database_mock.query.return_value = mocked_results

    suggestions = table.get_suggestions("blah", 10)

    assert len(suggestions) == 2
    database_mock.query.assert_called_with(Contains("ilike 'blah%'"))


@mock.patch("masquerade.providers.open_sgid.database")
def test_get_suggestions_numeric(database_mock):
    numeric_table = Table("table_name", "name", POLYGON, search_field_type=NUMERIC)
    mocked_results = [[1, "search text"], [2, "more search text"]]
    database_mock.query.return_value = mocked_results

    suggestions = numeric_table.get_suggestions("31", 10)

    assert len(suggestions) == 2
    database_mock.query.assert_called_with(Contains("= 31"))


@mock.patch("masquerade.providers.open_sgid.database")
def test_get_suggestions_numeric_with_text_in_query(database_mock):
    numeric_table = Table("table_name", "name", POLYGON, search_field_type=NUMERIC)
    mocked_results = [[1, "search text"], [2, "more search text"]]
    database_mock.query.return_value = mocked_results

    suggestions = numeric_table.get_suggestions("31 d", 10)

    assert len(suggestions) == 0
    database_mock.query.assert_not_called()


@mock.patch("masquerade.providers.open_sgid.database")
def test_get_candidate_from_magic_key(database_mock):
    mocked_result = [1, "match text", 1, 2, 3, 4, 5, 6, "value"]

    database_mock.get_magic_key_record.return_value = (
        mocked_result,
        [
            "xid",
            "search_field",
            "x",
            "y",
            "xmin",
            "xmax",
            "ymin",
            "ymax",
            "another_field",
        ],
    )

    candidate = table.get_candidate_from_magic_key(1, 3857)

    assert candidate["address"] == "match text"
    assert candidate["attributes"]["Score"] == 100
    assert candidate["location"]["x"] == 1
    assert candidate["location"]["y"] == 2
    assert candidate["extent"]["xmax"] == 3
    assert candidate["extent"]["ymax"] == 4
    assert candidate["extent"]["xmin"] == 5
    assert candidate["extent"]["ymin"] == 6


def test_get_magic_key_query():
    point_table = Table("point_table_name", "name", POINT)

    point_query = point_table.get_magic_key_query(1, 1234)

    #: manually expandes extent
    assert re.search("st_expand", point_query)

    polygon_table = Table("point_table_name", "name", POLYGON)

    polygon_table = polygon_table.get_magic_key_query(1, 1234)

    #: manually expandes extent
    assert re.search("st_expand", polygon_table) is None


def test_get_suggestion_from_record_with_context():
    suggestion = table.get_suggestion_from_record(
        1, "match text", "context value", "another value"
    )

    assert suggestion["text"] == "match text, context value, another value"


def test_address_points_normalizes_first_direction_in_suggestions():
    tests = [
        ("1234 North 1234 East", "1234 n 1234 east"),
        ("1234 No 1234 East", "1234 n 1234 east"),
        ("1234 So", "1234 s"),
        ("1235 Eas hello", "1235 e hello"),
        ("1235 E. hello", "1235 e hello"),
        ("1235 Ea. hello", "1235 e hello"),
        ("1234", "1234"),
    ]
    for input, expected in tests:
        text = normalize_prefix_direction(input)

        assert text == expected


@mock.patch("masquerade.providers.open_sgid.database")
def test_custom_get_suggestion_from_record(database_mock):
    table = Table(
        "tablename",
        "searchfield",
        POINT,
        get_suggestion_text_from_record=lambda matched_text, *rest: f"test {matched_text}",
    )

    mocked_result = [1, "match text", 1, 2, 3, 4, 5, 6, "value"]

    database_mock.get_magic_key_record.return_value = (
        mocked_result,
        [
            "xid",
            "search_field",
            "x",
            "y",
            "xmin",
            "xmax",
            "ymin",
            "ymax",
            "another_field",
        ],
    )

    candidate = table.get_candidate_from_magic_key(1, 3857)

    assert candidate["address"] == "test match text"
    assert candidate["attributes"]["Score"] == 100
