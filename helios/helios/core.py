# -*- coding: utf-8 -*-

""" Interacts with EOS db """

from pymongo import MongoClient

from models.query import MongoQuery, CollectionQueryBuilder


class EosQuery(MongoQuery):
    """ Specific query to EOS database """

    def _get_results(self):
        """
        :param args: extra args
        :param kwargs: extra kwargs
        :return: voids params -> just removes ID field in results
        """

        raw = self.driver.find(self.params, {'_id': False})
        return list(raw)  # auto convert to list


class EosQueryBuilder(CollectionQueryBuilder):
    """ Specific query builder for EOS database """

    # todo example only of a parameter pre-filled query field
    def withP0As(self, op, val):
        return self.withKeyAs('p0', op, val)

    def withP1As(self, op, val):
        return self.withKeyAs('p1', op, val)

    def build(self):
        query = EosQuery(self.params)
        query.set_driver(self.driver)

        return query


class Helios:
    def __init__(self, config):
        self.config = config
        self.query_builder = self._get_query_builder()

    def builder(self):
        return self.query_builder

    def _get_query_builder(self):
        client = MongoClient(
            self.config.get_db_server(),
            self.config.get_db_port()
        )

        return EosQueryBuilder(
            client,
            self.config.get_db_name(),
            self.config.get_files_collection_name()
        )
