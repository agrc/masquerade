#!/usr/bin/env python
# * coding: utf8 *
"""
A module that contains tests for masquerade.
"""

from json import dumps

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
