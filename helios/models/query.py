# -*- coding: utf-8 -*-


""" Queries EOS DB """

from enum import Enum


class MongoFilters(Enum):
    EQUALS = 'eq'
    NOT_EQUALS = 'ne'
    LESS_THAN = 'lt'
    LESS_THAN_OR_EQUAL_TO = 'lte'
    BIGGER_THAN = 'gt'
    BIGGER_THAN_OR_EQUAL_TO = 'gte'
    IN = 'in'
    NOT_IN = 'nin'


class QueryBuilder:
    def __init__(self):
        self.params = {}

    def withP0As(self, op, val):
        self.withKeyAs('p0', op, val)

    def withKeyAs(self, key, op, val):
        """
        :param key: key of doc
        :param val: val that doc.key should have ...
        :param op: ... according to this operator
        :return: void, saves params
        """

        mongo_operator = '${}'.format(op)
        self.params[key] = {
            mongo_operator: val
        }

    def build(self):
        return MongoQuery(self.params)


class MongoQuery:
    def __init__(self, params):
        self.collection = None
        self.params = params

    def _get_results(self):
        return self.collection.find(self.params)

    def execute(self, collection):
        self.collection = collection
        return self._get_results()
