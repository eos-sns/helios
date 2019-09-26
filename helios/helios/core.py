# -*- coding: utf-8 -*-

""" Interacts with EOS db """

import inspect

from pymongo import MongoClient

from helios.helios.io import AstraeusDataSaver
from helios.logs.logger import Logger
from helios.models.query.eos import EosQueryBuilder
from helios.models.query.sql import SqlQueryAdapter


class Helios:
    def __init__(self, config):
        self.config = config
        self.client = MongoClient(
            self.config.get_db_server(),
            self.config.get_db_port()
        )
        self.db_name = self.config.get_db_name()
        self.collection_name = self.config.get_coll_name()

        self.query_builder = self._get_query_builder()
        self.driver = self.client[self.db_name][self.collection_name]

        self.saver = AstraeusDataSaver(self.config.get_output())
        self.logger = Logger(self.__class__.__name__)  # unique ID + class name

    def with_params(self, raw_sql):
        try:
            query = SqlQueryAdapter().build(raw_sql)
            query.set_driver(self.query_builder.driver)

            return query
        except:
            raise ValueError('Cannot parse "{}" query'.format(raw_sql))

    def builder(self):
        return self.query_builder

    def save_to_disk(self, results):
        return self.saver.save_json(results)

    def get_download_link(self, val):
        return self.saver.get_download_key_for(val)

    def download(self, results):
        try:
            if len(results) > 1:
                return self.saver.download_multiple(results)

            return self.saver.download_as_json(results)
        except Exception as e:
            func_context = inspect.stack()[0]
            self.logger.log_error(func_context, e)

    def _get_query_builder(self):
        return EosQueryBuilder(
            self.client,
            self.db_name,
            self.collection_name
        )
