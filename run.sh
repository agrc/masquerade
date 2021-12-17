#!/bin/bash
set -e

source venv/bin/activate

flask run --cert=cert.pem --key=key.pem --host=0.0.0.0
