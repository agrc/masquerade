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
    """ tests info data and also assertions that are the same for all requests
    """
    response = test_client.get(f'{BASE_ROUTE}/info')

    #: assertions that are common for all requests (main.send_response)
    assert response.status_code == 200

    #: info-request specifics
    assert b'currentVersion' in response.data
    assert b'fullVersion' in response.data
    assert b'authInfo' in response.data


def test_base_geocode_route(test_client):
    response = test_client.get(GEOCODE_SERVER_ROUTE)

    assert response.status_code == 200

    assert b'currentVersion' in response.data
    assert b'singleLineAddressField' in response.data
    assert b'locatorProperties' in response.data


@mock.patch('masquerade.main.open_sgid.get_candidate_from_magic_key')
def test_find_candidates(get_candidate_mock, test_client):
    get_candidate_mock.return_value = 'blah'

    response = test_client.get(f'{GEOCODE_SERVER_ROUTE}/findAddressCandidates?magicKey=1&outSR={{"wkid": 102100}}')
    response_json = json.loads(response.data)

    assert response_json['candidates'][0] == 'blah'
    assert response_json['spatialReference']['latestWkid'] == 3857


@mock.patch('masquerade.main.open_sgid.get_candidate_from_magic_key')
def test_find_candidates_with_out_out_sr(get_candidate_mock, test_client):
    #: Pro doesn't include the outSR in these requests if the default matches the map
    get_candidate_mock.return_value = 'blah'

    response = test_client.get(f'{GEOCODE_SERVER_ROUTE}/findAddressCandidates?magicKey=1')
    response_json = json.loads(response.data)

    assert response_json['candidates'][0] == 'blah'
    assert response_json['spatialReference']['latestWkid'] == 4326
