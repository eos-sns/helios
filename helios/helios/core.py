# -*- coding: utf-8 -*-

""" Interacts with EOS db """

from pymongo import MongoClient

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
        self.collection_name = self.config.get_files_collection_name()

        self.query_builder = self._get_query_builder()
        self.driver = self.client[self.db_name][self.collection_name]

    def with_params(self, raw_sql):
        try:
            query = SqlQueryAdapter().build(raw_sql)
            query.set_driver(self.query_builder.driver)

            return query
        except:
            raise ValueError('Cannot parse "{}" query'.format(raw_sql))

    def builder(self):
        return self.query_builder

    def _get_query_builder(self):
        return EosQueryBuilder(
            self.client,
            self.db_name,
            self.collection_name
        )
