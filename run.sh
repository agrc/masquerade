#!/bin/bash
export FLASK_APP=src/masquerade/main.py
export FLASK_ENV=development
export WEB_API_KEY=$(<.apikey)
flask run --cert=cert.pem --key key.pem --host=0.0.0.0
