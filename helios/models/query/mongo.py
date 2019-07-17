# -*- coding: utf-8 -*-

from helios.models.mongo.config import MongoFilters
from helios.models.query.results import MongoResults


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

        raw = self._get_results()
        return MongoResults(raw)


class MongoQueryBuilder:
    AVAILABLE_MONGO_FILTERS = ', '.join(MongoFilters.availables())
    NOT_VALID_OPERATOR_FORMAT = '{} not a valid Mongo operator. Please user ' \
                                'one of the following: ' + \
                                AVAILABLE_MONGO_FILTERS

    def __init__(self, params=None):
        if not params:
            params = {}

        params = [
            {key: {
                op: val
            } for op, val in condition.items()}
            for key, condition in params.items()
        ]  # dict -> list of dicts
        self.params = {'$and': params}

    def set_key_as(self, key, op, val):
        mongo_operator = '${}'.format(op.value)  # get value from enum
        self.params['$and'].append({
            key: {
                mongo_operator: val
            }
        })  # add condition

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
