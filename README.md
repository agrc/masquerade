# agrc/masquerade

[![Build Status](https://travis-ci.com/agrc/masquerade.svg?branch=master)](https://travis-ci.com/agrc/masquerade)
[![codecov](https://codecov.io/gh/agrc/masquerade/branch/main/graph/badge.svg?token=R97EAY9FB1)](undefined)

A proxy service that creates an Esri locator from AGRC data and web services.

## URLs

- [Production](https://masquerade.ugrc.utah.gov/arcgis/rest/services/UtahLocator/GeocodeServer)
- [Staging](https://masquerade-gcedbtv4sa-uc.a.run.app/arcgis/rest/services/UtahLocator/GeocodeServer)
- [Local](https://localhost:5000/arcgis/rest/services/UtahLocator/GeocodeServer)

## Development

### One-time Setup

1. create new python environment: `python -m venv venv`
1. activate new environment: `source venv/bin/activate` (On Windows: `.env\Scripts\activate`)
1. install dependencies and editable project: `pip install -e ".[tests]"`
1. create `.env` (using `.env.sample` as a template) and populate this `WEB_API_KEY` variable with a newly created api key. Use type: `browser` and referer: `masquerade.agrc.utah.gov`.

#### MacOS

1. install [mkcert](https://github.com/FiloSottile/mkcert) `brew install mkcert`
1. run `mkcert -install`
1. create locally-trusted cert (from root): `mkcert -key-file key.pem -cert-file cert.pem localhost 127.0.0.1 10.211.55.2`
   - `10.211.55.2` is the default ip for the Parallels host machine
1. install the mkcert CA on another VM
   - copy `rootCA.pem` and `rootCA-key.pem` from the directory that is the output of `mkcert -CAROOT`
   - paste these files into a file on the VM
   - install mkcert on the VM
   - run `set CAROOT=<pasted directory> && mkcert -install` on the VM (windows terminal works better than a console emulator)

#### Windows

1. install [mkcert](https://github.com/FiloSottile/mkcert) `choco install mkcert`
1. run `mkcert -install`
1. create locally-trusted cert (from root): `mkcert -key-file key.pem -cert-file cert.pem localhost 127.0.0.1`

#### CI/CD

1. Run [the terraform code associated with this project](https://github.com/agrc/gcp-terraform/tree/main/masquerade).
1. Create `dev` and `prod` environments in GitHub repo.
1. Create repo-wide secrets:
   - `WEB_API_KEY`
   - `CODECOV_TOKEN`

1. create secrets in github for each environment

   - `PROJECT_ID`
   - Secrets contained in `github-actions-secrets-[prod/dev].txt` (output from terraform)

### Tests

(**P**ython **T**est **W**atch will restart the tests every time you save a file)

`ptw`

### Development Server

`./run.sh` (macOS) or `run.bat` (Windows)

[Here is a web app builder project](https://utah.maps.arcgis.com/apps/webappviewer/index.html?id=97a1529c31c84a93956968d48c6e08ad) that is pointed at `https://localhost:5000/` that can be used for testing.

### Deployment to GCP

When changes are pushed to either the `main` (production) or `staging` branches, the project is automatically built and deployed to the appropriate GCP project (pending passing tests).
