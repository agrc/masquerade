#!/usr/bin/env python
# * coding: utf8 *
"""
The main flask app
"""

import json

from dotenv import load_dotenv
from flask import Flask, redirect, request
from flask.logging import create_logger
from flask_cors import CORS
from flask_json import FlaskJSON, as_json_p

from .providers import open_sgid, web_api

load_dotenv()

BASE_ROUTE = '/arcgis/rest'
GEOCODE_SERVER_ROUTE = f'{BASE_ROUTE}/services/UtahLocator/GeocodeServer'
WGS84 = 4326
WEB_MERCATOR = 3857
OLD_WEB_MERCATOR = 102100
SERVER_VERSION_MAJOR = 10
SERVER_VERSION_MINOR = 8
SERVER_VERSION_PATCH = 1
DEFAULT_MAX_SUGGESTIONS = 50

app = Flask(__name__)
FlaskJSON(app)
CORS(app)
log = create_logger(app)


@app.after_request
def add_common_headers(response):
    """ add headers that we want returned with all requests
    """
    response.headers['Cache-Control'] = 'max-age=0,must-revalidate'

    return response


@app.route(f'{BASE_ROUTE}/info')
@as_json_p
def info():
    """ base info request
    """
    return {
        'currentVersion': f'{SERVER_VERSION_MAJOR}.{SERVER_VERSION_MINOR}{SERVER_VERSION_PATCH}',
        'fullVersion': f'{SERVER_VERSION_MAJOR}.{SERVER_VERSION_MINOR}.{SERVER_VERSION_PATCH}',
        'authInfo': {
            'isTokenBasedSecurity': False
        }
    }


@app.route(GEOCODE_SERVER_ROUTE)
@as_json_p
def geocode_base():
    """ base geocode server request
    """
    return {
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
    }


@app.route(f'{GEOCODE_SERVER_ROUTE}/suggest')
@as_json_p
def suggest():
    """ provide single-line address suggestions
    """

    search_text = request.args.get('text')
    max_results = request.args.get('maxSuggestions') or DEFAULT_MAX_SUGGESTIONS

    return {'suggestions': open_sgid.get_suggestions(search_text, max_results)}


@app.route(f'{GEOCODE_SERVER_ROUTE}/findAddressCandidates')
@as_json_p
def find_candidates():
    """ get address candidates from address points (if there is a magic key) or
    agrc geocoding service
    """

    magic_key = request.args.get('magicKey')

    out_sr_param_name = 'outSR'
    if out_sr_param_name in request.args:
        request_wkid = json.loads(request.args.get(out_sr_param_name))['wkid']
    else:
        request_wkid = WGS84

    #: switch out old mercator for new one otherwise, pass it through
    out_spatial_reference = WEB_MERCATOR if request_wkid == OLD_WEB_MERCATOR else request_wkid

    if magic_key is not None:
        candidate = open_sgid.get_candidate_from_magic_key(magic_key, out_spatial_reference)
        candidates = [candidate]
    else:
        single_line_address = request.args.get('Single Line Input')
        max_locations = request.args.get('maxLocations')
        candidates = web_api.get_address_candidates(single_line_address, out_spatial_reference, max_locations)

    return {'candidates': candidates, 'spatialReference': {'wkid': request_wkid, 'latestWkid': out_spatial_reference}}


@app.route(f'{GEOCODE_SERVER_ROUTE}/<path:path>', methods=['HEAD'])
def geocode_head(path):
    """ handle head requests from Pro
    """
    return path


@app.route('/')
def main():
    """ redirect to github project
    """
    return redirect('https://github.com/agrc/masquerade#agrcmasquerade')
