# agrc/masquerade

[![Build Status](https://travis-ci.com/agrc/masquerade.svg?branch=master)](https://travis-ci.com/agrc/masquerade)
[![Coverage Status](https://coveralls.io/repos/github/agrc/masquerade/badge.svg?branch=master)](https://coveralls.io/github/agrc/masquerade?branch=master)

A proxy service that creates an Esri locator from AGRC web services.

## Development

### One-time Setup

1. create new python environment: `python -m venv .env`
1. activate new environment: `source .env/bin/activate`
1. install dependencies and editable project: `pip install -e ".[tests]"`
1. generate self-signed cert for local https: `openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365`
1. add cert a always trust to mac os keychain:
   1. Open Keychain app -> Certificate
   1. Drag and drop `cert.pem`
   1. Right-click -> Get Info -> Trust -> "Always Trust"
   1. run server and go to https://localhost:5000 and click Advanced...

### Tests

(**P**ython **W**atch **T**est will restart the tests every time you save a file)

`pwt`

### Development Server

`export FLASK_APP=src/masquerade/main.py && flask run --cert=cert.pem --key key.pem`

Here is a web app builder project that is pointed at `https://127.0.0.1:5000/` that can be used for testing: https://utah.maps.arcgis.com/apps/webappviewer/index.html?id=97a1529c31c84a93956968d48c6e08ad
