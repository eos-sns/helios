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
        .with_key_as('ALPHA_ESC', MongoFilters.GREATER_THAN, -0.5) \
        .with_key_as('ALPHA_ESC', MongoFilters.LESS_THAN, -0.25) \
        .build()
    results = query.execute()
    results = results.get()  # get raw
    print(results)  # mmmh, not exaclty what I wanted, let's refine

    # results = results \
    #     .filter_by({'p0': {'>=': 2}}) \
    #     .filter_by('p0 > 1 and p2 <= 9')
    # print(results)  # yess, now let's save and download
    #
    # results = results.get()  # get raw
    # disk_path = helios.save_to_disk(results)  # saved in home folder
    # download_url = helios.download(results)  # now let's download


if __name__ == '__main__':
    main()
