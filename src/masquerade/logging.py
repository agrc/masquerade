#!/usr/bin/env python
# * coding: utf8 *
"""
A module for setting up logging
"""

import logging
import re

token_pattern = re.compile(r"(token=)([^&]+)", re.IGNORECASE)


class SensitiveDataFilter(logging.Filter):
    """redact sensitive data from log messages"""

    def filter(self, record):
        # Redact or remove sensitive data from the log record's message
        new_args = tuple(map(lambda arg: re.sub(token_pattern, r"\1<REDACTED>", arg), record.args))
        record.args = new_args

        return True


def initialize_logging():
    """initialize logging for the flask app"""
    logger = logging.getLogger("werkzeug")
    logger.addFilter(SensitiveDataFilter())
