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
    name='masquerade',
    version='1.1.7',
    license='MIT',
    description='A proxy service that creates an Esri locator from AGRC data and web services.',
    author='AGRC',
    author_email='agrc@utah.gov',
    url='https://github.com/agrc/masquerade',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    zip_safe=True,
    classifiers=[
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Utilities',
    ],
    project_urls={
        'Issue Tracker': 'https://github.com/agrc/masquerade/issues',
    },
    keywords=['gis'],
    install_requires=[
        'agrc-sweeper==1.3.*',
        'flask-cors==3.0.*',
        'Flask-JSON==0.3.*',
        'flask==2.2.*',
        'psycopg_pool==3.1.*',
        'psycopg[binary]==3.1.*',
        'python-dotenv==1.0.*',
        'requests==2.28.*',
        'tenacity==8.2.*',

        #: flask uses this by default if installed
        #: this handles decimals as returned from open sgid data better than the default json library
        'simplejson>=3.17,<3.19',
    ],
    extras_require={
        'tests': [
            'callee==0.3.*',
            'pylint-quotes==0.2.*',
            'pylint==2.17.*',
            'pytest-cov==4.0.*',
            'pytest-instafail==0.5.*',
            'pytest-isort>=3.0,<3.2',
            'pytest-pylint==0.19.*',
            'pytest-watch==4.2.*',
            'pytest>=7.1,<7.4',
            'requests-mock==1.10.*',
            'yapf==0.32.*',
        ]
    },
    setup_requires=[
        'pytest-runner',
    ],
    entry_points={'console_scripts': [
        'masquerade = masquerade.main:main',
    ]},
)
