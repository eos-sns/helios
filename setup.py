# !/usr/bin/python3
# -*- coding: utf-8 -*-


""" Install dependencies """

from setuptools import setup, find_packages

PACKAGE_NAME = 'Helios'
LITTLE_DESCRIPTION = 'Interact with EOS database'
DESCRIPTION = '{}: {}'.format(PACKAGE_NAME, LITTLE_DESCRIPTION)

setup(
    name=PACKAGE_NAME,
    version="1.0.1",
    description=LITTLE_DESCRIPTION,
    long_description=DESCRIPTION,
    keywords="eos",
    url="https://github.com/eos-sns/helios",
    packages=find_packages(exclude=["tests"]),
    include_package_data=True,
    install_requires=[
        'pymongo'
    ]
)
