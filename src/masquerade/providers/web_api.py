#!/usr/bin/env python
# * coding: utf8 *
"""
A module that contains methods for querying the AGRC geocoding service
"""
import os

import requests
from sweeper.address_parser import Address

WEB_API_URL = 'https://api.mapserv.utah.gov/api/v1/geocode'


def get_address_candidates(single_line_address, out_spatial_reference, max_locations):
    """ parses the single line address and passes it to the AGRC geocoding service
    and then returns the results as an array of candidates
    """

    try:
        parsed_address = Address(single_line_address)
    except Exception:
        return []

    parameters = {
        'apiKey': os.getenv('WEB_API_KEY'),
        'spatialReference': out_spatial_reference,
        'suggest': max_locations
    }

    headers = {'Referer': 'https://masquerade.agrc.utah.gov'}
    url = f'{WEB_API_URL}/{parsed_address.normalized}/{parsed_address.zip_code or parsed_address.city}'

    response = requests.get(url, params=parameters, headers=headers)

    if response.ok:
        result = response.json()['result']

        if result['score'] == 100:
            return [etl_candidate(result)]

        return [etl_candidate(candidate) for candidate in result['candidates']]

    response.raise_for_status()

    return []


def etl_candidate(agrc_candidate):
    """ translates an AGRC Web API candidate to an Esri locator candidate
    """
    address = agrc_candidate['address'] if 'address' in agrc_candidate else agrc_candidate['matchAddress']
    return {
        'address': address,
        'attributes': {
            'Score': agrc_candidate['score'],
            'locator': agrc_candidate['locator'],
            'addressGrid': agrc_candidate['addressGrid']
        },
        'location': agrc_candidate['location'],
        'Score': agrc_candidate['score']
    }
