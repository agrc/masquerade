#!/usr/bin/env python
# * coding: utf8 *
"""
test_masquerade.py
A module that contains tests for masquerade.
"""

from json import dumps

from masquerade.main import (
    ADDRESS_POINTS_FEATURE_SERVICE, BASE_ROUTE, GEOCODE_SERVER_ROUTE, OLD_WEB_MERCATOR, WEB_MERCATOR
)


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


def test_suggest(test_client, requests_mock):
    mocked_response = {
        'features': [
            {
                'attributes': {
                    'FullAdd': '123 E 100 N',
                    'OBJECTID': 356,
                    'AddSystem': 'GUNNISON',
                    'City': 'SANDY'
                }
            },
            {
                'attributes': {
                    'FullAdd': '123 E 300 S',
                    'OBJECTID': 511,
                    'AddSystem': 'GUNNISON',
                    'City': None
                }
            },
            {
                'attributes': {
                    'FullAdd': '123 E 200 S',
                    'OBJECTID': 526,
                    'AddSystem': 'GUNNISON',
                    'City': None
                }
            },
        ]
    }
    requests_mock.get(f'{ADDRESS_POINTS_FEATURE_SERVICE}/query', json=mocked_response)

    response = test_client.get(f'{GEOCODE_SERVER_ROUTE}/suggest', json={'text': '123'})

    assert response.status_code == 200

    response_json = response.get_json()

    assert len(response_json['suggestions']) == 3

    first_suggestion = response_json['suggestions'][0]

    assert first_suggestion['isCollection'] == False
    assert first_suggestion['magicKey'] == 356

    #: prefer city for zone value
    assert first_suggestion['text'] == '123 E 100 N, SANDY'

    #: fallback to address system if no city
    assert response_json['suggestions'][1]['text'] == '123 E 300 S, GUNNISON'


def test_find_candidate_with_magic_key(test_client, requests_mock):
    mocked_response = {
        'features': [{
            'attributes': {
                'FullAdd': '123 E 100 N',
                'OBJECTID': 356,
                'AddSystem': 'GUNNISON',
                'City': 'GUNNISON'
            },
            'geometry': {
                'x': -12447120.6022,
                'y': 4744161.701800004
            }
        }]
    }
    requests_mock.get(f'{ADDRESS_POINTS_FEATURE_SERVICE}/query', json=mocked_response)

    response = test_client.get(
        f'{GEOCODE_SERVER_ROUTE}/findAddressCandidates',
        query_string={
            'magicKey': 356,
            'outSR': dumps({'wkid': OLD_WEB_MERCATOR})
        }
    )

    assert response.status_code == 200

    response_json = response.get_json()

    assert len(response_json['candidates']) == 1
    assert response_json['candidates'][0]['address'] == '123 E 100 N, GUNNISON'
    assert response_json['candidates'][0]['attributes']['score'] == 100
    assert response_json['candidates'][0]['location'] is not None
    assert response_json['spatialReference']['latestWkid'] == WEB_MERCATOR
