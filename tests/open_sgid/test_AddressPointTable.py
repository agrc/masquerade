#!/usr/bin/env python
# * coding: utf8 *
"""
A module that contains tests for the open_sgid.AddressPointTable class
"""

from masquerade.providers.open_sgid import (
    ADDSYSTEM,
    CITY,
    FULLADD,
    POINT,
    AddressPointTable,
)

table = AddressPointTable(
    "table_name", FULLADD, POINT, additional_out_fields=[ADDSYSTEM, CITY]
)


def test_get_suggestion_from_record_with_city():
    suggestion = table.get_suggestion_from_record(
        1, "full_add", "address_system", "city"
    )

    assert suggestion["isCollection"] == False
    assert suggestion["magicKey"] == "1-table_name"
    assert suggestion["text"] == "full_add, city"


def test_get_suggestion_from_record_without_city():
    suggestion = table.get_suggestion_from_record(1, "full_add", "address_system", None)

    assert suggestion["isCollection"] == False
    assert suggestion["magicKey"] == "1-table_name"
    assert suggestion["text"] == "full_add, address_system"
