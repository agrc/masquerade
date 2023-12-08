#!/usr/bin/env python
# * coding: utf8 *
"""
Utility functions
"""
import json

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


def get_out_spatial_reference(incoming_request):
    """get the desired output spatial reference from the request"""
    out_sr_param_name = "outSR"

    if incoming_request.method == "GET":
        request_params = incoming_request.args
    else:
        request_params = incoming_request.form

    if out_sr_param_name in request_params:
        out_sr_param = request_params.get(out_sr_param_name)
        try:
            request_wkid = int(out_sr_param)
        except ValueError:
            request_wkid = json.loads(out_sr_param)["wkid"]
    else:
        request_wkid = WGS84

    #: switch out old mercator for new one otherwise, pass it through
    return (
        request_wkid,
        WEB_MERCATOR if request_wkid == OLD_WEB_MERCATOR else request_wkid,
    )
