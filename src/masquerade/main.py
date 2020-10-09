#!/usr/bin/env python
# * coding: utf8 *
"""
The main flask app
"""

import json

import requests
from flask import Flask, request
from flask.logging import create_logger
from flask_cors import CORS
from flask_jsonpify import jsonify

BASE_ROUTE = '/arcgis/rest'
GEOCODE_SERVER_ROUTE = f'{BASE_ROUTE}/services/UtahLocator/GeocodeServer'
SPATIAL_REFERENCE_WKID = 4326
ADDRESS_POINTS_FEATURE_SERVICE = (
    'https://services1.arcgis.com/99lidPhWCzftIe9K/ArcGIS/rest/services/UtahAddressPoints/FeatureServer/0/'
)
FULL_ADDRESS_FIELD = 'FullAdd'
OBJECTID = 'OBJECTID'
ADDRESS_SYSTEM_FIELD = 'AddSystem'
CITY_FIELD = 'City'
WEB_MERCATOR = 3857
OLD_WEB_MERCATOR = 102100
SERVER_VERSION_MAJOR = 10
SERVER_VERSION_MINOR = 8
SERVER_VERSION_PATCH = 1

app = Flask(__name__)
CORS(app)
log = create_logger(app)


@app.route(f'{BASE_ROUTE}/info')
def info():
    """ base info request
    """
    return jsonify({
        'currentVersion': f'{SERVER_VERSION_MAJOR}.{SERVER_VERSION_MINOR}{SERVER_VERSION_PATCH}',
        'fullVersion': f'{SERVER_VERSION_MAJOR}.{SERVER_VERSION_MINOR}.{SERVER_VERSION_PATCH}',
        'authInfo': {
            'isTokenBasedSecurity': False
        }
    })


@app.route(GEOCODE_SERVER_ROUTE)
def geocode_base():
    """ base geocode server request
    """
    return jsonify({
        'currentVersion': f'{SERVER_VERSION_MAJOR}.{SERVER_VERSION_MINOR}{SERVER_VERSION_PATCH}',
        'serviceDescription': 'Utah AGRC Locators wrapped with Masquerade',
        'addressFields': [{
            'name': 'Address',
            'type': 'esriFieldTypeString',
            'alias': 'Street Address',
            'required': False,
            'length': 100
        }, {
            'name': 'City',
            'type': 'esriFieldTypeString',
            'alias': 'City',
            'required': False,
            'length': 50
        }, {
            'name': 'Zip',
            'type': 'esriFieldTypeString',
            'alias': 'Zip',
            'required': False,
            'length': 10
        }],
        #: this was the key to WAB Search widget validation...
        'singleLineAddressField': {
            'name': 'Single Line Input',
            'type': 'esriFieldTypeString',
            'alias': 'Full Address',
            'required': False,
            'length': 150
        },
        'candidateFields': [],
        'spatialReference': {
            'wkid': SPATIAL_REFERENCE_WKID,
            'latestWkid': SPATIAL_REFERENCE_WKID
        },
        'locatorProperties': {
            'EndOffset': '0',
            'LoadBalancerTimeOut': 60,
            'MatchIfScoresTie': 'true',
            'MaxBatchSize': 100,
            'MinimumCandidateScore': '60',
            'MinimumMatchScore': '60',
            'SideOffset': '0',
            'SideOffsetUnits': 'ReferenceDataUnits',
            'SpellingSensitivity': '80',
            'SuggestedBatchSize': 50,
            'UICLSID': '{590C03A8-75C5-439D-84EE-726D235538DD}',
            'WritePercentAlongField': 'false',
            'WriteReferenceIDField': 'false',
            'WriteStandardizedAddressField': 'false',
            'WriteXYCoordFields': 'true'
        },
        'capabilities': ','.join(['Geocode', 'ReverseGeocode', 'Suggest'])
    })


def get_suggestion_from_address_point(feature):
    """ return a suggestion dictionary from an esri feature dictionary
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


@app.route(f'{GEOCODE_SERVER_ROUTE}/suggest')
def suggest():
    """ provide single-line address suggestions
    """
    feature_service_parameters = {
        'f': 'json',
        'where': f'{FULL_ADDRESS_FIELD} LIKE \'{request.args.get("text")}%\'',
        'outFields': ','.join([OBJECTID, FULL_ADDRESS_FIELD, ADDRESS_SYSTEM_FIELD, CITY_FIELD]),
        'returnGeometry': False,
        'orderByFields': [FULL_ADDRESS_FIELD],
        'resultType': 'standard',
        'resultRecordCount': 50
    }

    feature_service_response = requests.get(
        f'{ADDRESS_POINTS_FEATURE_SERVICE}/query', params=feature_service_parameters
    )

    feature_service_json = feature_service_response.json()

    suggestions = [get_suggestion_from_address_point(feature) for feature in feature_service_json['features']]

    return jsonify({'suggestions': suggestions})


@app.route(f'{GEOCODE_SERVER_ROUTE}/findAddressCandidates')
def find_candidates():
    """ get address candidates from address points (if there is a magic key) or
    agrc geocoding service
    """

    magic_key = request.args.get('magicKey')
    request_wkid = json.loads(request.args.get('outSR'))['wkid']

    if magic_key is not None:
        feature_service_parameters = {
            'f': 'json',
            'objectIds': magic_key,
            'returnGeometry': True,
            'outFields': ','.join([OBJECTID, FULL_ADDRESS_FIELD, ADDRESS_SYSTEM_FIELD, CITY_FIELD]),
            'outSR': WEB_MERCATOR if request_wkid == OLD_WEB_MERCATOR else request_wkid
        }

        feature_service_response = requests.get(
            f'{ADDRESS_POINTS_FEATURE_SERVICE}/query', params=feature_service_parameters
        )
        log.info('%s', feature_service_response.url)

        feature = feature_service_response.json()['features'][0]

        return jsonify({
            'candidates': [{
                'address': get_suggestion_from_address_point(feature)['text'],
                'attributes': {
                    'score': 100
                },
                'location': feature['geometry']
            }],
            'spatialReference': {
                'wkid': request_wkid,
                'latestWkid': feature_service_parameters['outSR']
            }
        })

    return 'not implemented'
