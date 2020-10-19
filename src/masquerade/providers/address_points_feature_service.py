#!/usr/bin/env python
# * coding: utf8 *
"""
A suggestion provider that queries the address points AGOL feature service
"""
import requests

FEATURE_SERVICE_URL = (
    'https://services1.arcgis.com/99lidPhWCzftIe9K/ArcGIS/rest/services/UtahAddressPoints/FeatureServer/0/'
)
FULL_ADDRESS_FIELD = 'FullAdd'
OBJECTID = 'OBJECTID'
ADDRESS_SYSTEM_FIELD = 'AddSystem'
CITY_FIELD = 'City'


def get_suggestion_from_feature(feature):
    """ return a suggestion dictionary based on an Esri feature dictionary
    """
    attributes = feature['attributes']

    if attributes[CITY_FIELD] is not None:
        zone = attributes[CITY_FIELD]
    else:
        zone = attributes[ADDRESS_SYSTEM_FIELD]

    return {
        'isCollection': False,
        'magicKey': attributes[OBJECTID],
        'text': f'{attributes[FULL_ADDRESS_FIELD]}, {zone}'
    }


def get_suggestions(search_text, max_results):
    """ queries the feature service and returns suggestions based on the input text
    """
    feature_service_parameters = {
        'f': 'json',
        'where': f'UPPER({FULL_ADDRESS_FIELD}) LIKE UPPER(\'{search_text}%\')',
        'outFields': ','.join([OBJECTID, FULL_ADDRESS_FIELD, ADDRESS_SYSTEM_FIELD, CITY_FIELD]),
        'returnGeometry': False,
        'orderByFields': [FULL_ADDRESS_FIELD],
        'resultType': 'standard',
        'resultRecordCount': max_results
    }

    feature_service_response = requests.get(f'{FEATURE_SERVICE_URL}/query', params=feature_service_parameters)

    feature_service_json = feature_service_response.json()

    return [get_suggestion_from_feature(feature) for feature in feature_service_json['features']]


def get_candidate_from_magic_key(magic_key, out_spatial_reference):
    """ queries the feature service for the feature corresponding to the magic key and
    returns it as an address candidate
    """
    feature_service_parameters = {
        'f': 'json',
        'objectIds': magic_key,
        'returnGeometry': True,
        'outFields': ','.join([OBJECTID, FULL_ADDRESS_FIELD, ADDRESS_SYSTEM_FIELD, CITY_FIELD]),
        'outSR': out_spatial_reference
    }

    feature_service_response = requests.get(f'{FEATURE_SERVICE_URL}/query', params=feature_service_parameters)

    feature = feature_service_response.json()['features'][0]

    return {
        'address': get_suggestion_from_feature(feature)['text'],
        'attributes': {
            'score': 100
        },
        'location': feature['geometry']
    }
