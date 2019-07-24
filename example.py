# !/usr/bin/python3

import os

from config.configuration import EosConfiguration
from helios.helios.core import Helios
from models.mongo.config import MongoFilters

HERE = os.path.abspath(os.path.dirname(__file__))
DEFAULT_CONFIG_FOLDER = os.path.join(HERE, 'config')
DEFAULT_CONFIG_FILE = os.path.join(DEFAULT_CONFIG_FOLDER, 'config.json')  # ./config/config.json


def main():
    configuration = EosConfiguration(DEFAULT_CONFIG_FILE)
    helios = Helios(configuration)
    query = helios.builder() \
        .with_key_as('ALPHA_ESC', MongoFilters.GREATER_THAN, -1.5) \
        .with_key_as('ALPHA_ESC', MongoFilters.LESS_THAN, -0.2) \
        .build()
    results = query.execute()
    results = results.get()  # get raw
    print(results)  # mmmh, not exactly what I wanted, let's refine

    disk_path = helios.download(results)
    print(disk_path)


if __name__ == '__main__':
    main()
