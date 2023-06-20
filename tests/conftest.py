#!/usr/bin/env python
# * coding: utf8 *
"""
conftest.py
A module that defines fixtures for pytest
"""

from pytest import fixture

from masquerade import main


@fixture(scope="module")
def test_client():
    """
    provide a test client for the flask app
    """
    flask_app = main.app
    testing_client = flask_app.test_client()

    yield testing_client
