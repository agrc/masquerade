# agrc/masquerade

[![Build Status](https://travis-ci.com/agrc/masquerade.svg?branch=master)](https://travis-ci.com/agrc/masquerade)
[![Coverage Status](https://coveralls.io/repos/github/agrc/masquerade/badge.svg?branch=master)](https://coveralls.io/github/agrc/masquerade?branch=master)

A proxy service that creates an Esri locator from AGRC data and web services.

## Development

### One-time Setup

1. create new python environment: `python -m venv .env`
1. activate new environment: `source .env/bin/activate`
1. install dependencies and editable project: `pip install -e ".[tests]"`
1. install [mkcert](https://github.com/FiloSottile/mkcert) `brew install mkcert`
1. create locally-trusted cert: `mkcert -key-file key.pem -cert-file cert.pem localhost 127.0.0.1`
1. create `.apikey` and populate it with the Web API key for this project.

### Tests

(**P**ython **W**atch **T**est will restart the tests every time you save a file)

`pwt`

### Development Server

`./run.sh`

[Here is a web app builder project](https://utah.maps.arcgis.com/apps/webappviewer/index.html?id=97a1529c31c84a93956968d48c6e08ad) that is pointed at `https://localhost:5000/` that can be used for testing.

### Deployment to GCP

`./deploy.sh` (you will be prompted for the project name)
