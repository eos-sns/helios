# -*- coding: utf-8 -*-

from enum import Enum


class MongoFilters(Enum):
    EQUALS = 'eq'
    NOT_EQUALS = 'ne'
    LESS_THAN = 'lt'
    LESS_THAN_OR_EQUAL_TO = 'lte'
    GREATER_THAN = 'gt'
    GREATER_THAN_OR_EQUAL_TO = 'gte'
    IN = 'in'
    NOT_IN = 'nin'

    @staticmethod
    def availables():
        return [e.value for e in MongoFilters]


class MongoQuery:
    CANNOT_USE_DRIVER_FORMAT = 'Mongo driver not specified! Please use ' \
                               '`set_driver(...)`'

    def __init__(self, params, driver=None):
        self.driver = driver
        self.params = params

    def set_driver(self, driver):
        self.driver = driver

    def _get_results(self):
        if not self.driver:
            raise ValueError(self.CANNOT_USE_DRIVER_FORMAT)

        raw = self.driver.find(self.params)
        return list(raw)

    def execute(self, driver=None):
        if driver:
            self.set_driver(driver)

        return self._get_results()


class MongoQueryBuilder:
    AVAILABLE_MONGO_FILTERS = ', '.join(MongoFilters.availables())
    NOT_VALID_OPERATOR_FORMAT = '{} not a valid Mongo operator. Please user ' \
                                'one of the following: ' + \
                                AVAILABLE_MONGO_FILTERS

    def __init__(self, params=None):
        if not params:
            params = {}

        self.params = params

    def set_key_as(self, key, op, val):
        if not isinstance(op, MongoFilters):
            raise ValueError(self.NOT_VALID_OPERATOR_FORMAT.format(op))

        op = op.value  # get value from enum
        mongo_operator = '${}'.format(op)
        self.params[key] = {
            mongo_operator: float(val)
        }

    def with_key_as(self, key, op, val):
        """
        :param key: key of doc
        :param val: val that doc.key should have ...
        :param op: ... according to this operator. Must be an instance of
        MongoFilters
        :return: void, saves params
        """

        self.set_key_as(key, op, val)
        return self

    def build(self, query_class=MongoQuery):
        return query_class(self.params)
