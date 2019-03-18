# !/usr/bin/python3
# -*- coding: utf-8 -*-

""" Interacts with EOS db """

import argparse
import os

from helios.config.configuration import Configuration
from helios.helios.core import Helios
from helios.logs.logger import get_custom_logger
from helios.models.query.mongo import MongoFilters

LOGGER = get_custom_logger('CLI')
HERE = os.path.abspath(os.path.dirname(__file__))
UP_HERE = os.path.dirname(HERE)
DEFAULT_CONFIG_FOLDER = os.path.join(UP_HERE, 'config')
DEFAULT_CONFIG_FILE = os.path.join(DEFAULT_CONFIG_FOLDER, 'db.json')


def create_args():
    """
    :return: ArgumentParser
        Parser that handles cmd arguments.
    """

    parser = argparse.ArgumentParser(usage='-h for full usage')

    parser.add_argument('-c', dest='config_file',
                        help='configuration file', required=False,
                        default=DEFAULT_CONFIG_FILE)

    return parser


def parse_args(parser):
    """
    :param parser: ArgumentParser
        Object that holds cmd arguments.
    :return: tuple
        Values of arguments.
    """

    args = parser.parse_args()

    config_file = str(args.config_file)
    assert os.path.exists(config_file)

    return config_file


def main():
    config_file = parse_args(create_args())  # parse mode

    configuration = Configuration(config_file)  # parse config file

    helios = Helios(configuration)
    query = helios.builder() \
        .with_p0_as(MongoFilters.LESS_THAN, 11) \
        .with_p1_as(MongoFilters.GREATER_THAN, 1) \
        .build()
    results = query.execute()
    print(results)

    query = helios.with_params('p0 < 11 and p1 > 1')
    results = query.execute()
    print(results)

    results = results \
        .filter_by({'p0': {'>=': 2}}) \
        .filter_by('p0 > 1 and p2 <= 9')
    print(results)


if __name__ == '__main__':
    main()
