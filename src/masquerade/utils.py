#!/usr/bin/env python
# * coding: utf8 *
"""
Utility functions
"""


def cleanse_text(text):
    """ removes leading or trailing spaces and quotes
    """
    if text is None:
        return None

    if not isinstance(text, str):
        return text

    return text.strip().replace('"', '').replace('\'', '')
