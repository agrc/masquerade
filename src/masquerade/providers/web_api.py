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
from flask import current_app
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


def make_geocode_request(address: str, zone: str, out_spatial_reference: int, max_locations: int) -> list:
    """makes a request to the web api geocoding service"""
    parameters = {
        "apiKey": os.getenv("WEB_API_KEY"),
        "spatialReference": out_spatial_reference,
        "suggest": max_locations,
    }

    url = f"{BASE_URL}/geocode/{_cleanse_street(address)}/{_cleanse_zone(zone)}"

    response = session.get(url, params=parameters, headers=HEADERS, timeout=10)

    candidates = []

    if response.status_code == 404 and "no address candidates found" in response.text.lower():
        return candidates

    if response.ok:
        try:
            result = response.json()["result"]
        except Exception:
            current_app.warning(f"Error parsing web api geocoding result: {response.text}")
            return candidates

        if "score" in result:
            if result["score"] >= MIN_SCORE_FOR_BATCH:
                candidates.append(etl_candidate(result, out_spatial_reference))
                #: if the score is 100 then we can skip the rest of the candidates
                if result["score"] == 100:
                    return candidates

        if "candidates" in result:
            candidates += [etl_candidate(candidate, out_spatial_reference) for candidate in result["candidates"]]

        return candidates

    response.raise_for_status()

    return candidates


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


def etl_candidate(ugrc_candidate: dict, spatial_reference: int) -> dict:
    """translates an UGRC Web API candidate to an Esri locator candidate"""
    address = ugrc_candidate["address"] if "address" in ugrc_candidate else ugrc_candidate["matchAddress"]

    match_city = address.split(",")[-1].strip()
    city_or_county = open_sgid.get_city(
        ugrc_candidate["location"]["x"], ugrc_candidate["location"]["y"], spatial_reference
    )
    if not city_or_county:
        city_or_county = open_sgid.get_county(
            ugrc_candidate["location"]["x"], ugrc_candidate["location"]["y"], spatial_reference
        )
        if city_or_county:
            city_or_county = f"{city_or_county} COUNTY"

    if city_or_county and match_city.upper() != city_or_county.upper():
        address = address.replace(match_city, city_or_county.upper())

    try:
        web_api_standardized_address = ugrc_candidate["standardizedAddress"]
        standardized_address = (
            f"{' '.join([part.title() for part in web_api_standardized_address.split(' ')])}, {city_or_county}"
        )
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


def reverse_geocode(x: float, y: float, spatial_reference: int, input_x: float, input_y: float) -> dict:
    """reverse geocodes a point using web api supplemented by open sgid queries"""

    city = open_sgid.get_city(x, y, spatial_reference)
    city = city.upper() if city else None
    county = open_sgid.get_county(x, y, spatial_reference)
    if county:
        county = f"{county} COUNTY"
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
        "Subregion": county,
        "Region": "UTAH",
        "RegionAbbr": "UT",
        "Territory": "",  # unused by masquerade
        "Postal": zip_code or "",
        "PostalExt": "",  # unused by masquerade
        "CntryName": "UNITED STATES",
        "CountryCode": "USA",
        "X": x,
        "Y": y,
        "InputX": input_x,
        "InputY": input_y,
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
            current_app.warning(f"Error parsing web api reverse geocode result: {response.text}")
            return result

        street = api_result["address"]["street"]
        address_type = api_result["address"]["addressType"]
        match_address = f"{street}, {city or county}, UTAH, {zip_code}"

        result["Match_addr"] = match_address
        result["LongLabel"] = f"{match_address}, USA"
        result["ShortLabel"] = street
        result["Addr_type"] = address_type
        result["AddNum"] = street.split(" ")[0]
        result["Address"] = street

    return result
