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

    response = test_client.get(
        f'{GEOCODE_SERVER_ROUTE}/findAddressCandidates?magicKey=1-table&outSR={{"wkid": 102100}}'
    )
    response_json = json.loads(response.data)

    assert response_json['candidates'][0] == 'blah'
    assert response_json['spatialReference']['latestWkid'] == 3857


def test_find_candidates_invalid_magic_key(test_client):
    response = test_client.get(f'{GEOCODE_SERVER_ROUTE}/findAddressCandidates?magicKey=invalid')

    assert response.status_code == 400
    assert b'Invalid magicKey' in response.data


@mock.patch('masquerade.main.open_sgid.get_candidate_from_magic_key')
def test_find_candidates_with_out_out_sr(get_candidate_mock, test_client):
    #: Pro doesn't include the outSR in these requests if the default matches the map
    get_candidate_mock.return_value = 'blah'

    response = test_client.get(f'{GEOCODE_SERVER_ROUTE}/findAddressCandidates?magicKey=1-table')
    response_json = json.loads(response.data)

    assert response_json['candidates'][0] == 'blah'
    assert response_json['spatialReference']['latestWkid'] == 4326


def test_head_requests(test_client):
    response = test_client.head(f'{GEOCODE_SERVER_ROUTE}/Masquerade/UtahLocator%20(10.211.55.2:5000)')

    assert response.status_code == 200
    assert response.headers['Cache-Control']


def test_can_handle_bad_values(test_client):
    response = test_client.get(f'{GEOCODE_SERVER_ROUTE}/suggest?text=123&maxSuggestions=undefined')

    assert response.status_code == 200

    response_json = json.loads(response.data)

    assert len(response_json['suggestions']) > 0


def test_batch_can_handle_missing_addresses(test_client):
    response = test_client.post(
        f'{GEOCODE_SERVER_ROUTE}/geocodeAddresses',
        data={
            'addresses': dumps({
                'records': [{
                    'attributes': {
                        'OBJECTID': 1,
                        'Zip': '84043'
                    }
                }, {
                    'attributes': {
                        'OBJECTID': 2,
                        'Zip': '84043'
                    }
                }]
            })
        }
    )

    assert response.status_code == 200

    response_json = json.loads(response.data)

    assert len(response_json['locations']) == 2
    assert response_json['locations'][0]['address'] == None
    assert response_json['locations'][1]['address'] == None
