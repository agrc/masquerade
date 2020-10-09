#!/usr/bin/env python
# * coding: utf8 *
"""
The main flask app
"""

import json

from flask import Flask, request
from flask.logging import create_logger
from flask_cors import CORS
from flask_jsonpify import jsonify

from .providers import address_points_feature_service

BASE_ROUTE = '/arcgis/rest'
GEOCODE_SERVER_ROUTE = f'{BASE_ROUTE}/services/UtahLocator/GeocodeServer'
WGS84 = 4326
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
            'wkid': WGS84,
            'latestWkid': WGS84
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


@app.route(f'{GEOCODE_SERVER_ROUTE}/suggest')
def suggest():
    """ provide single-line address suggestions
    """

    return jsonify({'suggestions': address_points_feature_service.get_suggestions(request.args.get('text'))})


@app.route(f'{GEOCODE_SERVER_ROUTE}/findAddressCandidates')
def find_candidates():
    """ get address candidates from address points (if there is a magic key) or
    agrc geocoding service
    """

    magic_key = request.args.get('magicKey')
    request_wkid = json.loads(request.args.get('outSR'))['wkid']
    out_spatial_reference = WEB_MERCATOR if request_wkid == OLD_WEB_MERCATOR else request_wkid

    if magic_key is not None:
        candidate = address_points_feature_service.get_candidate_from_magic_key(magic_key, out_spatial_reference)

        return jsonify({
            'candidates': [candidate],
            'spatialReference': {
                'wkid': request_wkid,
                'latestWkid': out_spatial_reference
            }
        })

    raise NotImplementedError
