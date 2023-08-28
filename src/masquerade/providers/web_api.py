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

WEB_API_URL = "https://api.mapserv.utah.gov/api/v1/geocode"
MIN_SCORE_FOR_BATCH = 70


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

    return make_request(parsed_address.normalized, zone, out_spatial_reference, max_locations)


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
            "x-ugrc-geocode-client": "masquerade",
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


def make_request(address, zone, out_spatial_reference, max_locations):
    """makes a request to the web api geocoding service"""
    parameters = {
        "apiKey": os.getenv("WEB_API_KEY"),
        "spatialReference": out_spatial_reference,
        "suggest": max_locations,
    }

    headers = {"Referer": "https://masquerade.ugrc.utah.gov"}
    url = f"{WEB_API_URL}/{_cleanse_street(address)}/{_cleanse_zone(zone)}"

    response = session.get(url, params=parameters, headers=headers, timeout=10)

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

    candidates = make_request(address, zone, out_spatial_reference, 1)

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
