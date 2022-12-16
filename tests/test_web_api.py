#!/usr/bin/env python
# * coding: utf8 *
"""
A module that contains methods for testing the web_api module
"""
import re

from pytest import raises

from masquerade.providers.web_api import (
    WEB_API_URL, etl_candidate, get_candidate_from_parts, get_candidates_from_single_line
)


def test_etl_candidate():
    input = {
        'address': '3989 SOUTH FRONTAGE RD, Salt Lake City',
        'location': {
            'x': 416707.62244415266,
            'y': 4508458.9846219225
        },
        'score': 69.92,
        'locator': 'Centerlines.StatewideRoads',
        'addressGrid': 'Salt Lake City'
    }

    result = etl_candidate(input)

    assert result['address'] == input['address']
    assert result['attributes']['score'] == 69.92
    assert result['attributes']['locator'] == input['locator']
    assert result['attributes']['addressGrid'] == input['addressGrid']
    assert result['location'] == input['location']


def test_etl_candidate_base_result():
    #: this is a test for the base result object as opposed to result.candidate objects
    input = {
        'location': {
            'x': 429340.24421129236,
            'y': 4504146.207401402
        },
        'score': 100,
        'locator': 'Centerlines.StatewideRoads',
        'matchAddress': '3987 S 1925 E, Salt Lake City',
        'inputAddress': '3987 s 1925 e, 84124',
        'standardizedAddress': '3987 south 1925 east',
        'addressGrid': 'Salt Lake City',
        'candidates': []
    }

    result = etl_candidate(input)

    assert result['address'] == input['matchAddress']
    assert result['score'] == 100
    assert result['attributes']['locator'] == input['locator']
    assert result['attributes']['addressGrid'] == input['addressGrid']
    assert result['location'] == input['location']


def test_get_address_candidate(requests_mock):
    mock_response = {
        'result': {
            'location': {
                'x': -12455627.277556794,
                'y': 4977968.997941715
            },
            'score': 90.92,
            'locator': 'AddressPoints.AddressGrid',
            'matchAddress': '123 S MAIN ST, SALT LAKE CITY',
            'inputAddress': '123 s main, 84115',
            'standardizedAddress': '123 south main',
            'addressGrid': 'SALT LAKE CITY',
            'candidates': [{
                'address': '123 S MAIN ST, Salt Lake City',
                'location': {
                    'x': -12455641.089194497,
                    'y': 4977985.769253134
                },
                'score': 90.92,
                'locator': 'Centerlines.StatewideRoads',
                'addressGrid': 'Salt Lake City'
            }, {
                'address': '123 E MAIN ST, SALT LAKE CITY',
                'location': {
                    'x': -12455160.88511952,
                    'y': 4952534.59547376
                },
                'score': 83.35,
                'locator': 'AddressPoints.AddressGrid',
                'addressGrid': 'SALT LAKE CITY'
            }, {
                'address': '123 N MAIN ST, Salt Lake City',
                'location': {
                    'x': -12455681.168985613,
                    'y': 4978777.601108425
                },
                'score': 83.35,
                'locator': 'Centerlines.StatewideRoads',
                'addressGrid': 'Salt Lake City'
            }, {
                'address': '124 S MAIN ST, Salt Lake City',
                'location': {
                    'x': -12455680.654925054,
                    'y': 4977979.505714583
                },
                'score': 69.92,
                'locator': 'Centerlines.StatewideRoads',
                'addressGrid': 'Salt Lake City'
            }, {
                'address': '123 S MAIN ST, HOLDEN',
                'location': {
                    'x': -12497885.87723581,
                    'y': 4735613.7251902325
                },
                'score': 66.89,
                'locator': 'AddressPoints.AddressGrid',
                'addressGrid': 'HOLDEN'
            }]
        },
        'status': 200
    }

    requests_mock.get(re.compile(f'{WEB_API_URL}.*'), json=mock_response)
    candidates = get_candidates_from_single_line('123 s main, 84115', 3857, 5)

    assert len(candidates) == 5


def test_get_address_candidate_perfect_match(requests_mock):
    mock_response = {
        'result': {
            'location': {
                'x': -12455627.277556794,
                'y': 4977968.997941715
            },
            'score': 100,
            'locator': 'AddressPoints.AddressGrid',
            'matchAddress': '123 S MAIN ST, SALT LAKE CITY',
            'inputAddress': '123 s main st, 84115',
            'standardizedAddress': '123 south main street',
            'addressGrid': 'SALT LAKE CITY',
            'candidates': [{
                'address': '123 S MAIN ST, Salt Lake City',
                'location': {
                    'x': -12455641.089194497,
                    'y': 4977985.769253134
                },
                'score': 100,
                'locator': 'Centerlines.StatewideRoads',
                'addressGrid': 'Salt Lake City'
            }, {
                'address': '123 E MAIN ST, SALT LAKE CITY',
                'location': {
                    'x': -12455160.88511952,
                    'y': 4952534.59547376
                },
                'score': 92.43,
                'locator': 'AddressPoints.AddressGrid',
                'addressGrid': 'SALT LAKE CITY'
            }, {
                'address': '123 N MAIN ST, Salt Lake City',
                'location': {
                    'x': -12455681.168985613,
                    'y': 4978777.601108425
                },
                'score': 92.43,
                'locator': 'Centerlines.StatewideRoads',
                'addressGrid': 'Salt Lake City'
            }, {
                'address': '124 S MAIN ST, Salt Lake City',
                'location': {
                    'x': -12455680.654925054,
                    'y': 4977979.505714583
                },
                'score': 79,
                'locator': 'Centerlines.StatewideRoads',
                'addressGrid': 'Salt Lake City'
            }, {
                'address': '124 N MAIN ST, Salt Lake City',
                'location': {
                    'x': -12455641.603544854,
                    'y': 4978783.717783414
                },
                'score': 71.43,
                'locator': 'Centerlines.StatewideRoads',
                'addressGrid': 'Salt Lake City'
            }]
        },
        'status': 200
    }

    requests_mock.get(re.compile(f'{WEB_API_URL}.*'), json=mock_response)
    candidates = get_candidates_from_single_line('123 s main st, 84115', 3857, 5)

    assert len(candidates) == 1
    assert candidates[0]['score'] == 100


def test_get_address_candidate_single_result_for_batch(requests_mock):
    mock_response = {
        'result': {
            'location': {
                'x': -12455627.277556794,
                'y': 4977968.997941715
            },
            'score': 80,
            'locator': 'AddressPoints.AddressGrid',
            'matchAddress': '123 S MAIN ST, SALT LAKE CITY',
            'inputAddress': '123 s main st, 84115',
            'standardizedAddress': '123 south main street',
            'addressGrid': 'SALT LAKE CITY'
        },
        'status': 200
    }

    requests_mock.get(re.compile(f'{WEB_API_URL}.*'), json=mock_response)
    candidate = get_candidate_from_parts('123 s main st', '84115', 3857)

    assert candidate['score'] == 80


def test_get_address_candidate_no_candidates(requests_mock):
    mock_response = {
        'result': {
            'location': {
                'x': -12455627.277556794,
                'y': 4977968.997941715
            },
            'score': 0,
            'locator': 'AddressPoints.AddressGrid',
            'matchAddress': '123 S MAIN ST, SALT LAKE CITY',
            'inputAddress': '123 s main st, 84115',
            'standardizedAddress': '123 south main street',
            'addressGrid': 'SALT LAKE CITY'
        },
        'status': 200
    }

    requests_mock.get(re.compile(f'{WEB_API_URL}.*'), json=mock_response)
    candidate = get_candidate_from_parts('123 s main st', '84115', 3857)

    assert candidate is None


def test_get_address_candidates_raises(requests_mock):
    requests_mock.get(re.compile(f'{WEB_API_URL}.*'), json={}, status_code=500)

    with raises(Exception):
        get_candidates_from_single_line('123 s main street, 84114', 3857, 5)


def test_get_address_candidates_bad_address(requests_mock):
    requests_mock.get(
        re.compile(f'{WEB_API_URL}.*'),
        json={
            "status": 404,
            "message": "No address candidates found with a score of 70 or better."
        },
        status_code=404
    )

    candidates = get_candidates_from_single_line('123 bad address, city name', 3857, 5)

    assert len(candidates) == 0

    candidates = get_candidates_from_single_line('0101300036', 3857, 5)

    assert len(candidates) == 0
