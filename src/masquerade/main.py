#!/usr/bin/env python
# * coding: utf8 *
"""
The main flask app
"""

import json
import random
import time

from dotenv import load_dotenv
from flask import Flask, redirect, request
from flask.logging import create_logger
from flask_cors import CORS
from flask_json import FlaskJSON, as_json_p
from requests.models import HTTPError

from .providers import open_sgid, web_api
from .utils import WGS84, cleanse_text, get_out_spatial_reference, get_request_param

load_dotenv()

BASE_ROUTE = "/arcgis/rest"
GEOCODE_SERVER_ROUTE = f"{BASE_ROUTE}/services/UtahLocator/GeocodeServer"
ADMIN_BASE_ROUTE = "/arcgis/admin"
SERVER_VERSION_MAJOR = 10
SERVER_VERSION_MINOR = 8
SERVER_VERSION_PATCH = 1
DEFAULT_MAX_SUGGESTIONS = 50
RATE_LIMIT_SECONDS = (0.015, 0.03)
BATCH_SIZE = 25

app = Flask(__name__)
FlaskJSON(app)
CORS(app)
log = create_logger(app)


@app.after_request
def add_common_headers(response):
    """add headers that we want returned with all requests"""
    response.headers["Cache-Control"] = "max-age=0,must-revalidate"

    return response


@app.route(f"{BASE_ROUTE}/info", methods=["GET", "POST"])
@as_json_p
def info():
    """base info request"""
    return {
        "currentVersion": f"{SERVER_VERSION_MAJOR}.{SERVER_VERSION_MINOR}{SERVER_VERSION_PATCH}",
        "fullVersion": f"{SERVER_VERSION_MAJOR}.{SERVER_VERSION_MINOR}.{SERVER_VERSION_PATCH}",
        "authInfo": {"isTokenBasedSecurity": False},
    }


@app.route(GEOCODE_SERVER_ROUTE, methods=["GET", "POST"])
@app.route(f"{GEOCODE_SERVER_ROUTE}/Masquerade", methods=["GET", "POST"])
@as_json_p
def geocode_base():
    """base geocode server request"""
    return {
        "addressFields": [
            {
                "name": "Address",
                "type": "esriFieldTypeString",
                "alias": "Street Address",
                "required": False,
                "length": 100,
            },
            {
                "name": "City",
                "type": "esriFieldTypeString",
                "alias": "City",
                "required": False,
                "length": 50,
            },
            {
                "name": "Zip",
                "type": "esriFieldTypeString",
                "alias": "Zip",
                "required": False,
                "length": 10,
            },
        ],
        "candidateFields": [
            {
                "name": "matchAddress",
                "type": "esriFieldTypeString",
                "alias": "Match Address",
                "required": False,
                "length": 160,
            },
            {
                "name": "score",
                "type": "esriFieldTypeDouble",
                "alias": "Score",
                "required": True,
            },
            {
                "name": "standardizedAddress",
                "type": "esriFieldTypeString",
                "alias": "Standardized Address",
                "required": False,
                "length": 160,
            },
            {
                "name": "locator",
                "type": "esriFieldTypeString",
                "alias": "Locator",
                "required": False,
                "length": 32,
            },
            {
                "name": "addressGrid",
                "type": "esriFieldTypeString",
                "alias": "Address Grid",
                "required": False,
                "length": 32,
            },
            {
                "name": "Shape",
                "type": "esriFieldTypeGeometry",
                "alias": "Shape",
                "required": True,
            },
        ],
        "capabilities": ",".join(["Geocode", "Suggest"]),
        "countries": ["US"],
        "currentVersion": f"{SERVER_VERSION_MAJOR}.{SERVER_VERSION_MINOR}{SERVER_VERSION_PATCH}",
        "locatorProperties": {
            "EndOffset": "0",
            "LoadBalancerTimeOut": 60,
            "MatchIfScoresTie": "true",
            "MaxBatchSize": BATCH_SIZE,
            "MinimumCandidateScore": "60",
            "MinimumMatchScore": "60",
            "SideOffset": "0",
            "SideOffsetUnits": "ReferenceDataUnits",
            "SpellingSensitivity": "80",
            "SuggestedBatchSize": BATCH_SIZE,
            "UICLSID": "{590C03A8-75C5-439D-84EE-726D235538DD}",
            "WritePercentAlongField": "false",
            "WriteReferenceIDField": "false",
            "WriteStandardizedAddressField": "false",
            "WriteXYCoordFields": "true",
        },
        "serviceDescription": "Utah Geospatial Resource Center locators wrapped with Masquerade",
        #: this was the key to WAB Search widget validation...
        "singleLineAddressField": {
            "name": "Single Line Input",
            "type": "esriFieldTypeString",
            "alias": "Full Address",
            "required": False,
            "length": 150,
        },
        "spatialReference": {"wkid": WGS84, "latestWkid": WGS84},
    }


@app.route(f"{ADMIN_BASE_ROUTE}/<path:path>.MapServer")
def geocode_map_server(path):
    """return 403 just like world geocoder

    maybe this just let's Pro know that there is no map server for this service
    """
    return f"no map server available for this service: {path}", 403


@app.route(f"{GEOCODE_SERVER_ROUTE}/suggest", methods=["GET", "POST"])
@as_json_p
def suggest():
    """provide single-line address suggestions"""

    search_text = get_request_param(request, "text")
    max_results = get_request_param(request, "maxSuggestions") or DEFAULT_MAX_SUGGESTIONS
    if isinstance(max_results, str):
        max_results = DEFAULT_MAX_SUGGESTIONS

    return {"suggestions": open_sgid.get_suggestions(cleanse_text(search_text), max_results)}


@app.route(f"{GEOCODE_SERVER_ROUTE}/findAddressCandidates", methods=["GET", "POST"])
@as_json_p
def find_candidates():
    """get address candidates from address points (if there is a magic key) or
    ugrc geocoding service
    """

    magic_key = get_request_param(request, "magicKey")

    request_wkid, out_spatial_reference = get_out_spatial_reference(request)

    if magic_key is not None:
        if open_sgid.SPLITTER not in magic_key:
            return f"Invalid magicKey: {magic_key}", 400

        candidate = open_sgid.get_candidate_from_magic_key(magic_key, out_spatial_reference)
        candidates = [candidate]
    else:
        single_line_address = cleanse_text(get_request_param(request, "Single Line Input"))
        max_locations = get_request_param(request, "maxLocations")
        try:
            candidates = web_api.get_candidates_from_single_line(
                single_line_address, out_spatial_reference, max_locations
            )
        except Exception as error:
            return {
                "error": {
                    "code": 500,
                    "message": "Error getting candidates from web api",
                    "details": [str(error)],
                }
            }, 500

    return {
        "candidates": candidates,
        "spatialReference": {
            "wkid": request_wkid,
            "latestWkid": out_spatial_reference,
        },
    }


@app.route(f"{GEOCODE_SERVER_ROUTE}/geocodeAddresses", methods=["GET", "POST"])
@as_json_p
def geocode_addresses():
    """geocode a batch of addresses"""

    request_wkid, out_spatial_reference = get_out_spatial_reference(request)

    addresses = json.loads(get_request_param(request, "addresses"))

    locations = []

    for address in addresses["records"]:
        time.sleep(random.uniform(*RATE_LIMIT_SECONDS))
        no_match = {
            "address": None,
            "attributes": {
                "ResultID": address["attributes"]["OBJECTID"],
                "Status": "U",
            },
        }

        #: single-line input
        keys = address["attributes"].keys()
        if "Zip" not in keys and "City" not in keys:
            candidate = web_api.get_candidate_from_single_line(address["attributes"]["Address"], out_spatial_reference)

            if candidate is None:
                locations.append(no_match)
            else:
                candidate["attributes"]["ResultID"] = address["attributes"]["OBJECTID"]
                locations.append(candidate)

            continue

        #: prefer zip over city and return no match if neither is passed
        try:
            zone = cleanse_text(address["attributes"]["Zip"])
        except KeyError:
            try:
                zone = cleanse_text(address["attributes"]["City"])
            except KeyError:
                locations.append(no_match)
                continue

        try:
            candidate = web_api.get_candidate_from_parts(
                cleanse_text(address["attributes"]["Address"]),
                zone,
                out_spatial_reference,
            )

            if candidate is None:
                candidate = no_match
            else:
                candidate["attributes"]["ResultID"] = address["attributes"]["OBJECTID"]
        except (HTTPError, KeyError):
            candidate = no_match

        locations.append(candidate)

    return {
        "locations": locations,
        "spatialReference": {
            "wkid": request_wkid,
            "latestWkid": out_spatial_reference,
        },
    }


@app.route(f"{GEOCODE_SERVER_ROUTE}/<path:path>", methods=["HEAD"])
def geocode_head(path):
    """handle head requests from Pro"""
    return path


@app.route("/")
def main():
    """redirect to github project"""
    return redirect("https://github.com/agrc/masquerade")
