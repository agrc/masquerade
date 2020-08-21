#!/usr/bin/env python
# * coding: utf8 *
"""
test_masquerade.py
A module that contains tests for the project module.
"""

from masquerade import main


def test_hello_returns_hi():
    assert main.hello() == 'hi'
