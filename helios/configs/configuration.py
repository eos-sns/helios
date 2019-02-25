#!/usr/bin/env python3
# coding: utf-8

""" Configuration module """

import json

from logs.logger import get_custom_logger


class Configuration:
    def __init__(self, config_file):
        self.config_file = config_file
        self.data = None  # will be a dictionary when parsed
        self.logger = get_custom_logger('CONFIGURATION')

    def _parse(self):
        self.logger.log_message('parse', self.config_file)
        raise NotImplementedError

    def get_config(self, key):
        if not self.data:  # cache
            with open(self.config_file) as reader:
                self.data = json.load(reader)

        return self.data[key]

    def get_matrioska_config(self, matrioska):
        """
        :param matrioska: list of inner configs, e.g ['db', 'coll', 'name']
        :return: None or value in config
        """

        current_matrioska = self.get_config(matrioska[0])

        for key in matrioska[1:]:  # first key already got
            try:
                current_matrioska = current_matrioska[key]
            except:
                return None

        return current_matrioska

    def get_db_name(self):
        return self.get_matrioska_config(['db', 'name'])

    def get_source_folder_of(self, key):
        return self.get_matrioska_config([key, 'files folder'])

    def get_file_format_of(self, key):
        return self.get_matrioska_config([key, 'file format'])

    def get_simulation_id_regex(self):
        return self.get_matrioska_config(['simulation', 'id regex'])

    def get_walker_collection_name(self):
        return self.get_matrioska_config(['Walker', 'collection name'])

    def get_tau_collection_name(self):
        return self.get_matrioska_config(['TauData', 'collection name'])
