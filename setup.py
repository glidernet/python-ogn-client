#!/usr/bin/env python3

from os import path
from setuptools import setup, find_packages

from ogn.gateway.settings import PACKAGE_VERSION


here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='ogn-python',
    version=PACKAGE_VERSION,
    description='A python module for the Open Glider Network',
    long_description=long_description,
    url='https://github.com/glidernet/ogn-python',
    author='Konstantin Gründger aka Meisterschueler, Fabian P. Schmidt aka kerel',
    author_email='kerel-fs@gmx.de',
    license='AGPLv3',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: GIS',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='gliding ogn',
    packages=find_packages(exclude=['tests', 'tests.*']),
    install_requires=[
        'SQLAlchemy==1.0.8',
        'geopy==1.11.0',
        'manage.py==0.2.10',
        'celery[redis]>=3.1,<3.2',
        'alembic==0.8.3'
    ],
    extras_require={
        'dev': [
            'nose==1.3.7',
            'coveralls==0.4.4',
            'flake8==2.5.0'
        ],
        'postgresql': [
            'psycopg2==2.6.1'
        ]
    },
    zip_safe=False
)
