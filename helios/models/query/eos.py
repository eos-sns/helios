# -*- coding: utf-8 -*-

from models.query.core import CollectionMongoQueryBuilder
from models.query.mongo import MongoQuery


class EosQuery(MongoQuery):
    """ Specific query to EOS database """

    def _get_results(self):
        """
        :return: removes ID field in results
        """

        raw = self.driver.find(self.params, {'_id': False})
        return list(raw)  # auto convert to list


class EosQueryBuilder(CollectionMongoQueryBuilder):
    """ Specific query builder for EOS database """

    # todo example only of a parameter pre-filled query field
    def with_p0_as(self, op, val):
        return self.with_key_as('p0', op, val)

    def with_p1_as(self, op, val):
        return self.with_key_as('p1', op, val)

    def build(self):
        query = EosQuery(self.params)
        query.set_driver(self.driver)

        return query
