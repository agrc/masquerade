#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
setup.py
A module that installs masquerade as a module
"""

from glob import glob
from os.path import basename, splitext

from setuptools import find_packages, setup

setup(
    name="masquerade",
    version="1.5.8",
    license="MIT",
    description="A proxy service that creates an Esri locator from UGRC data and web services.",
    author="UGRC",
    author_email="ugrc-developers@utah.gov",
    url="https://github.com/agrc/masquerade",
    packages=find_packages("src"),
    package_dir={"": "src"},
    py_modules=[splitext(basename(path))[0] for path in glob("src/*.py")],
    include_package_data=True,
    zip_safe=True,
    classifiers=[
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Utilities",
    ],
    project_urls={
        "Issue Tracker": "https://github.com/agrc/masquerade/issues",
    },
    keywords=["gis"],
    install_requires=[
        "ugrc-sweeper==2.*",
        "flask-cors==6.*",
        "Flask-JSON==0.4.*",
        "flask==3.*",
        "psycopg_pool==3.*",
        "psycopg[binary]==3.*",
        "pyproj==3.*",
        "python-dotenv==1.*",
        "requests==2.*",
        #: flask uses this by default if installed
        #: this handles decimals as returned from open sgid data better than the default json library
        "simplejson==3.*",
        "tenacity==9.*",
    ],
    extras_require={
        "tests": [
            "callee==0.3.*",
            "pytest-cov==6.*",
            "pytest-instafail==0.5.*",
            "pytest-watch==4.*",
            "pytest==8.*",
            "requests-mock==1.*",
            "ruff==0.*",
        ]
    },
    setup_requires=[
        "pytest-runner",
    ],
    entry_points={
        "console_scripts": [
            "masquerade = masquerade.main:main",
        ]
    },
)
