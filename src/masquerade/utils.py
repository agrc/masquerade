#!/usr/bin/env python
# * coding: utf8 *
"""
Utility functions
"""

import json

from flask import Request
from markupsafe import escape

WGS84 = 4326
WEB_MERCATOR = 3857
OLD_WEB_MERCATOR = 102100


def cleanse_text(text):
    """removes leading or trailing spaces and quotes"""
    if text is None:
        return None

    if not isinstance(text, str):
        return text

    return text.strip().replace('"', "").replace("'", "")


def get_request_param(request, param_name):
    """get the parameter from the request checking both url params and form data"""
    if param_name in request.args:
        return request.args.get(param_name)

    return request.form.get(param_name)


def get_out_spatial_reference(incoming_request: Request) -> tuple[int, int]:
    """get the desired output spatial reference from the request"""
    out_sr_param_name = "outSR"

    param_value = get_request_param(incoming_request, out_sr_param_name)

    if param_value is not None:
        try:
            request_wkid = int(param_value)
        except ValueError:
            request_wkid = json.loads(param_value)["wkid"]
    else:
        request_wkid = WGS84

    #: switch out old mercator for new one otherwise, pass it through
    return (
        request_wkid,
        WEB_MERCATOR if request_wkid == OLD_WEB_MERCATOR else request_wkid,
    )


def escape_while_preserving_numbers(value: int | float | str) -> int | float | str:
    """escape a value while preserving numbers"""
    if isinstance(value, (int, float)):
        return value

    return escape(value)
