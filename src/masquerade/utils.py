#!/usr/bin/env python
# * coding: utf8 *
"""
Utility functions
"""


def cleanse_text(text):
    """ removes leading or trailing spaces and quotes
    """
    return text.strip().replace('"', '').replace('\'', '')
