#!/usr/bin/env python
# * coding: utf8 *
"""
A module that contains methods for querying the UGRC geocoding service

This module shares a fair amount of code with this one:
https://github.com/agrc/geocoding-toolbox/blob/master/src/agrcgeocoding/geocode.py
"""

import os
import re

import requests
from requests.adapters import HTTPAdapter
from sweeper.address_parser import Address
from urllib3.util.retry import Retry

from . import open_sgid

BASE_URL = "https://api.mapserv.utah.gov/api/v1"
MIN_SCORE_FOR_BATCH = 70
HEADERS = {"Referer": "https://masquerade.ugrc.utah.gov"}


def get_candidates_from_single_line(single_line_address, out_spatial_reference, max_locations):
    """parses the single line address and passes it to the UGRC geocoding service
    and then returns the results as an array of candidates
    """

    try:
        parsed_address = Address(single_line_address)
    except Exception:
        return []

    zone = parsed_address.zip_code or parsed_address.city
    if not zone or not parsed_address.normalized:
        return []

    return make_geocode_request(parsed_address.normalized, zone, out_spatial_reference, max_locations)


ALLOWABLE_CHARS = re.compile("[^a-zA-Z0-9]")
SPACES = re.compile(" +")


def _cleanse_street(data):
    """cleans up address garbage"""
    replacement = " "

    #: & -> and
    street = data.replace(chr(38), "and")
    street = ALLOWABLE_CHARS.sub(replacement, street)
    street = SPACES.sub(replacement, street)

    return street.strip()


def _cleanse_zone(data):
    """cleans up zone garbage"""
    zone = ALLOWABLE_CHARS.sub(" ", str(data))
    zone = SPACES.sub(" ", zone).strip()

    if len(zone) > 0 and zone[0] == "8":
        zone = zone.strip()[:5]

    return zone


def _get_retry_session():
    """create a requests session that has a retry built into it"""
    retries = 3
    backoff_factor = 0.3
    status_forcelist = (500, 502, 504)

    new_session = requests.Session()
    new_session.headers.update(
        {
            "x-agrc-geocode-client": "masquerade",
        }
    )
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    new_session.mount("https://", adapter)

    return new_session


session = _get_retry_session()


def make_geocode_request(address, zone, out_spatial_reference, max_locations):
    """makes a request to the web api geocoding service"""
    parameters = {
        "apiKey": os.getenv("WEB_API_KEY"),
        "spatialReference": out_spatial_reference,
        "suggest": max_locations,
    }

    url = f"{BASE_URL}/geocode/{_cleanse_street(address)}/{_cleanse_zone(zone)}"

    response = session.get(url, params=parameters, headers=HEADERS, timeout=10)

    if response.status_code == 404 and "no address candidates found" in response.text.lower():
        return []

    if response.ok:
        try:
            result = response.json()["result"]
        except Exception:
            print(f"Error parsing result: {response.text}")
            return []

        if "score" in result:
            if result["score"] == 100 or max_locations == 1 and result["score"] >= MIN_SCORE_FOR_BATCH:
                return [etl_candidate(result)]

        if "candidates" in result:
            return [etl_candidate(candidate) for candidate in result["candidates"]]

        return []

    response.raise_for_status()

    return []


def get_candidate_from_parts(address, zone, out_spatial_reference):
    """gets a single candidate from address & zone input"""

    candidates = make_geocode_request(address, zone, out_spatial_reference, 1)

    if len(candidates) > 0:
        return candidates[0]

    return None


def get_candidate_from_single_line(single_line_address, out_spatial_reference):
    """gets a single candidate from a single line address input"""

    candidates = get_candidates_from_single_line(single_line_address, out_spatial_reference, 1)

    if len(candidates) > 0:
        return candidates[0]

    return None


def etl_candidate(ugrc_candidate):
    """translates an UGRC Web API candidate to an Esri locator candidate"""
    address = ugrc_candidate["address"] if "address" in ugrc_candidate else ugrc_candidate["matchAddress"]
    try:
        standardized_address = ugrc_candidate["standardizedAddress"]
    except KeyError:
        standardized_address = None

    return {
        "address": address,
        "attributes": {
            "Status": "M",
            "matchAddress": address,
            "score": ugrc_candidate["score"],
            "standardizedAddress": standardized_address,
            "locator": ugrc_candidate["locator"],
            "addressGrid": ugrc_candidate["addressGrid"],
        },
        "location": ugrc_candidate["location"],
        "score": ugrc_candidate["score"],
    }


def reverse_geocode(x, y, spatial_reference):
    """reverse geocodes a point using web api supplemented by open sgid queries"""

    city = open_sgid.get_city(x, y, spatial_reference)
    city = city.upper() if city else None
    county = open_sgid.get_county(x, y, spatial_reference)
    zip_code = open_sgid.get_zip(x, y, spatial_reference)

    #: example esri result: https://geocode.arcgis.com/arcgis/rest/services/World/GeocodeServer/reverseGeocode?location=%7B%22spatialReference%22%3A%7B%22wkid%22%3A102100%7D%2C%22x%22%3A-12452539.51148021%2C%22y%22%3A4947846.054923615%7D&f=json
    result = {
        "Match_addr": "",
        "LongLabel": "",
        "ShortLabel": "",
        "Addr_type": "",
        "Type": "",  # unused by masquerade
        "AddNum": "",
        "Address": "",
        "Block": "",  # unused by masquerade
        "Sector": "",  # unused by masquerade
        "Neighborhood": "",  # unused by masquerade
        "District": "",  # unused by masquerade
        "City": city or "",
        "MetroArea": "",  # unused by masquerade
        "Subregion": county or "",
        "Region": "UTAH",
        "RegionAbbr": "UT",
        "Territory": "",  # unused by masquerade
        "Postal": zip_code or "",
        "PostalExt": "",  # unused by masquerade
        "CntryName": "UNITED STATES",
        "CountryCode": "USA",
        "X": x,
        "Y": y,
        "InputX": x,
        "InputY": y,
    }

    parameters = {
        "apiKey": os.getenv("WEB_API_KEY"),
        "spatialReference": spatial_reference,
    }
    url = f"{BASE_URL}/geocode/reverse/{x}/{y}"
    response = session.get(url, params=parameters, headers=HEADERS, timeout=10)

    if response.status_code == 200 and response.ok:
        try:
            api_result = response.json()["result"]
        except Exception:
            print(f"Error parsing result: {response.text}")
            return None

        street = api_result["address"]["street"]
        address_type = api_result["address"]["addressType"]
        match_address = f"{street}, {city or f'{county} COUNTY'}, UTAH, {zip_code}"

        result["Match_addr"] = match_address
        result["LongLabel"] = f"{match_address}, USA"
        result["ShortLabel"] = street
        result["Addr_type"] = address_type
        result["AddNum"] = street.split(" ")[0]
        result["Address"] = street

    return result
