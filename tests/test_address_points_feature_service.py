#!/usr/bin/env python
# * coding: utf8 *
"""
A module that contains tests for the address_points_feature_service provider
"""
from masquerade.main import OLD_WEB_MERCATOR
from masquerade.providers.address_points_feature_service import (
    FEATURE_SERVICE_URL, get_candidate_from_magic_key, get_suggestions
)


def test_get_suggestions(test_client, requests_mock):
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
    requests_mock.get(f'{FEATURE_SERVICE_URL}/query', json=mocked_response)

    suggestions = get_suggestions('123')

    assert len(suggestions) == 3

    first_suggestion = suggestions[0]

    assert first_suggestion['isCollection'] == False
    assert first_suggestion['magicKey'] == 356

    #: prefer city for zone value
    assert first_suggestion['text'] == '123 E 100 N, SANDY'

    #: fallback to address system if no city
    assert suggestions[1]['text'] == '123 E 300 S, GUNNISON'


def test_get_candidate_from_magic_key(test_client, requests_mock):
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
    requests_mock.get(f'{FEATURE_SERVICE_URL}/query', json=mocked_response)

    candidate = get_candidate_from_magic_key(356, OLD_WEB_MERCATOR)

    assert candidate['address'] == '123 E 100 N, GUNNISON'
    assert candidate['attributes']['score'] == 100
    assert candidate['location'] is not None
