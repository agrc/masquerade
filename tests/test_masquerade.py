#!/usr/bin/env python
# * coding: utf8 *
"""
A module that contains tests for masquerade.
"""

from json import dumps
from unittest import mock

from flask import json

from masquerade.main import BASE_ROUTE, GEOCODE_SERVER_ROUTE


def test_info(test_client):
    """tests info data and also assertions that are the same for all requests"""
    response = test_client.get(f"{BASE_ROUTE}/info")

    #: assertions that are common for all requests (main.send_response)
    assert response.status_code == 200

    #: info-request specifics
    assert b"currentVersion" in response.data
    assert b"fullVersion" in response.data
    assert b"authInfo" in response.data


def test_base_geocode_route(test_client):
    response = test_client.get(GEOCODE_SERVER_ROUTE)

    assert response.status_code == 200

    assert b"currentVersion" in response.data
    assert b"singleLineAddressField" in response.data
    assert b"locatorProperties" in response.data


def test_geocode_bad_request(test_client):
    response = test_client.get(f"{GEOCODE_SERVER_ROUTE}/geocodeAddresses", query_string={"addresses": "not a list"})

    assert response.status_code == 400
    assert b"not valid JSON" in response.data


@mock.patch("masquerade.main.open_sgid.get_candidate_from_magic_key")
def test_find_candidates(get_candidate_mock, test_client):
    get_candidate_mock.return_value = "blah"

    response = test_client.get(
        f'{GEOCODE_SERVER_ROUTE}/findAddressCandidates?magicKey=1-table&outSR={{"wkid": 102100}}'
    )
    response_json = json.loads(response.data)

    assert response_json["candidates"][0] == "blah"
    assert response_json["spatialReference"]["latestWkid"] == 3857

    response = test_client.post(
        f"{GEOCODE_SERVER_ROUTE}/findAddressCandidates",
        data={"magicKey": "1-table", "outSR": '{"wkid": 102100}'},
    )
    response_json = json.loads(response.data)

    assert response_json["candidates"][0] == "blah"
    assert response_json["spatialReference"]["latestWkid"] == 3857


@mock.patch("masquerade.main.web_api.get_candidates_from_single_line")
def test_find_candidates_max_locations(get_candidates_mock, test_client):
    get_candidates_mock.return_value = ["blah"]

    response = test_client.get(
        f'{GEOCODE_SERVER_ROUTE}/findAddressCandidates?singleLine=address&outSR={{"wkid": 102100}}&maxLocations=1'
    )
    response_json = json.loads(response.data)

    assert response_json["candidates"][0] == "blah"
    assert get_candidates_mock.call_args.args[2] == 1


@mock.patch("masquerade.main.web_api.get_candidates_from_single_line")
def test_find_candidates_max_locations_bad_value(get_candidates_mock, test_client):
    get_candidates_mock.return_value = ["blah"]

    response = test_client.get(
        f'{GEOCODE_SERVER_ROUTE}/findAddressCandidates?singleLine=address&outSR={{"wkid": 102100}}&maxLocations=nope'
    )

    assert response.status_code == 400
    assert b"maxLocations" in response.data


@mock.patch("masquerade.main.web_api.get_candidates_from_single_line")
def test_find_candidates_single_line_variations(get_candidates_mock, test_client):
    get_candidates_mock.return_value = ["blah"]

    test_client.get(f'{GEOCODE_SERVER_ROUTE}/findAddressCandidates?SingleLine=address&outSR={{"wkid": 102100}}')

    assert get_candidates_mock.call_args.args[0] == "address"

    get_candidates_mock.reset_mock()

    test_client.get(
        f'{GEOCODE_SERVER_ROUTE}/findAddressCandidates?Single%20Line%20Input=address2&outSR={{"wkid": 102100}}'
    )

    assert get_candidates_mock.call_args.args[0] == "address2"


def test_find_candidates_invalid_magic_key(test_client):
    response = test_client.get(f"{GEOCODE_SERVER_ROUTE}/findAddressCandidates?magicKey=invalid")

    assert response.status_code == 400
    assert b"Invalid magicKey" in response.data


@mock.patch("masquerade.main.open_sgid.get_candidate_from_magic_key")
def test_find_candidates_with_out_out_sr(get_candidate_mock, test_client):
    #: Pro doesn't include the outSR in these requests if the default matches the map
    get_candidate_mock.return_value = "blah"

    response = test_client.get(f"{GEOCODE_SERVER_ROUTE}/findAddressCandidates?magicKey=1-table")
    response_json = json.loads(response.data)

    assert response_json["candidates"][0] == "blah"
    assert response_json["spatialReference"]["latestWkid"] == 4326


def test_head_requests(test_client):
    response = test_client.head(f"{GEOCODE_SERVER_ROUTE}/Masquerade/UtahLocator%20(10.211.55.2:5000)")

    assert response.status_code == 200
    assert response.headers["Cache-Control"]


def test_can_handle_bad_values(test_client):
    response = test_client.get(f"{GEOCODE_SERVER_ROUTE}/suggest?text=123&maxSuggestions=undefined")

    assert response.status_code == 200

    response_json = json.loads(response.data)

    assert len(response_json["suggestions"]) > 0


def test_batch_can_handle_missing_addresses(test_client):
    response = test_client.post(
        f"{GEOCODE_SERVER_ROUTE}/geocodeAddresses",
        data={
            "addresses": dumps(
                {
                    "records": [
                        {"attributes": {"OBJECTID": 1, "Zip": "84043"}},
                        {"attributes": {"OBJECTID": 2, "Zip": "84043"}},
                    ]
                }
            )
        },
    )

    assert response.status_code == 200

    response_json = json.loads(response.data)

    assert len(response_json["locations"]) == 2
    assert response_json["locations"][0]["address"] is None
    assert response_json["locations"][1]["address"] is None


@mock.patch("masquerade.main.web_api.get_candidate_from_single_line")
def test_batch_single_line(get_candidate_mock, test_client):
    get_candidate_mock.return_value = {
        "attributes": {},
        "address": "123 Main St",
    }

    response = test_client.post(
        f"{GEOCODE_SERVER_ROUTE}/geocodeAddresses",
        data={
            "addresses": dumps(
                {
                    "records": [
                        {"attributes": {"OBJECTID": 1, "Address": "123 Main St, Lehi"}},
                        {"attributes": {"OBJECTID": 2, "Address": "123 Main St, Lehi"}},
                    ]
                }
            )
        },
    )

    assert response.status_code == 200

    response_json = json.loads(response.data)

    assert len(response_json["locations"]) == 2
    assert response_json["locations"][0]["address"] is not None
    assert response_json["locations"][1]["address"] is not None


@mock.patch("masquerade.main.web_api.get_candidate_from_parts")
def test_batch_separate_fields(get_candidate_mock, test_client):
    get_candidate_mock.return_value = {
        "attributes": {},
        "address": "123 Main St",
    }

    response = test_client.post(
        f"{GEOCODE_SERVER_ROUTE}/geocodeAddresses",
        data={
            "addresses": dumps(
                {
                    "records": [
                        {"attributes": {"OBJECTID": 1, "Address": "123 Main St", "City": "Lehi"}},
                        {"attributes": {"OBJECTID": 2, "Address": "123 Main St", "Zip": 84043}},
                    ]
                }
            )
        },
    )

    assert response.status_code == 200

    response_json = json.loads(response.data)

    assert len(response_json["locations"]) == 2
    assert response_json["locations"][0]["address"] is not None
    assert response_json["locations"][1]["address"] is not None


def test_can_handle_output_sr_in_numeric_form(test_client):
    response = test_client.get(f"{GEOCODE_SERVER_ROUTE}/findAddressCandidates?outSR=4326&singleLine:hello")

    assert response.status_code == 200

    response_json = json.loads(response.data)

    assert response_json["spatialReference"]["latestWkid"] == 4326


@mock.patch("masquerade.main.web_api.reverse_geocode")
def test_reverse_geocode(reverse_geocode_mock, test_client):
    reverse_geocode_mock.return_value = {
        "address": "123 Main St",
    }
    response = test_client.get(
        f"{GEOCODE_SERVER_ROUTE}/reverseGeocode",
        query_string={
            "location": dumps({"spatialReference": {"wkid": 102100}, "x": -12448301.645792466, "y": 4947055.905820554})
        },
    )

    assert response.status_code == 200

    response_json = json.loads(response.data)

    assert response_json["address"]["address"] == "123 Main St"
    assert response_json["location"]["spatialReference"]["wkid"] == 4326


@mock.patch("masquerade.main.web_api.reverse_geocode")
def test_reverse_geocode_output_spatial_reference(reverse_geocode_mock, test_client):
    reverse_geocode_mock.return_value = {
        "address": "123 Main St",
    }
    response = test_client.get(
        f"{GEOCODE_SERVER_ROUTE}/reverseGeocode",
        query_string={
            "location": dumps({"spatialReference": {"wkid": 102100}, "x": -12448301.645792466, "y": 4947055.905820554}),
            "outSR": 26912,
        },
    )

    assert response.status_code == 200

    response_json = json.loads(response.data)

    assert response_json["address"]["address"] == "123 Main St"
    assert response_json["location"]["spatialReference"]["wkid"] == 26912
