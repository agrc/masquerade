#!/usr/bin/env python
# * coding: utf8 *
"""
A module for setting up logging
"""

import logging
import re

from flask.logging import create_logger

token_pattern = re.compile(r"token=([^&]+)")


class SensitiveDataFilter(logging.Filter):
    """redact sensitive data from log messages"""

    def __init__(self, pattern):
        super().__init__()
        self.pattern = pattern

    def filter(self, record):
        # Redact or remove sensitive data from the log record's message
        record.msg = re.sub(self.pattern, "REDACTED", record.msg)

        return True


def initialize_logging(app):
    """initialize logging for the flask app

    Args:
        app (Flask): The Flask app
    """
    logger = create_logger(app)
    logger.addFilter(SensitiveDataFilter(re.compile(r"token=([^&]+)", re.IGNORECASE)))
