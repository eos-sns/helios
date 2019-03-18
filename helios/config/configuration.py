# coding: utf-8

""" Configuration module """

import json
import os

from helios.logs.logger import get_custom_logger


class Configuration:
    DEFAULT = {
        'db': {
            'name': 'eos',
            'files collection name': 'files',
            'server': 'localhost',
            'port': 27017
        },
        'out': {
            'folder': os.path.join(os.getenv('HOME'), 'eos-data'),
            'url': 'https://eos.sns.it/download?token='
        }
    }

    def __init__(self, config_file):
        self.config_file = config_file
        self.data = None  # will be a dictionary when parsed
        self.logger = get_custom_logger('CONFIGURATION')

    def _parse(self):
        with open(self.config_file) as reader:
            self.data = json.load(reader)

    def get_config(self, key):
        if not self.data:  # cache
            self._parse()

        return self.data[key]

    def get_matrioska_config(self, matrioska):
        """
        :param matrioska: list of inner config, e.g ['db', 'coll', 'name']
        :return: None or value in config
        """

        current_matrioska = self.get_config(matrioska[0])

        for key in matrioska[1:]:  # first key already got
            try:
                current_matrioska = current_matrioska[key]
            except:
                return None

        return current_matrioska

    def get_db_info(self):
        return self.get_config('db')

    def get_files_collection_name(self):
        return self.get_matrioska_config(['db', 'files collection name'])

    def get_db_name(self):
        return self.get_matrioska_config(['db', 'name'])

    def get_db_server(self):
        return self.get_matrioska_config(['db', 'server'])

    def get_db_port(self):
        return self.get_matrioska_config(['db', 'port'])

    def get_source_folder_of(self, key):
        return self.get_matrioska_config([key, 'folder'])

    def get_file_format_of(self, key):
        return self.get_matrioska_config([key, 'file regex'])

    def get_simulation_id_regex(self):
        return self.get_matrioska_config(['simulation', 'id regex'])

    def get_walker_collection_name(self):
        return self.get_matrioska_config(['Walker', 'collection name'])

    def get_tau_collection_name(self):
        return self.get_matrioska_config(['TauData', 'collection name'])

    def get_output(self):
        return self.get_config('out')

    @staticmethod
    def default():
        conf = Configuration(None)
        conf.data = Configuration.DEFAULT
        return conf
