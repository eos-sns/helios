# -*- coding: utf-8 -*-


""" Queries EOS DB """

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


class QueryBuilder:
    AVAILABLE_MONGO_FILTERS = ', '.join(MongoFilters.availables())
    NOT_VALID_OPERATOR_FORMAT = '{} not a valid Mongo operator. Please user ' \
                                'one of the following: ' + \
                                AVAILABLE_MONGO_FILTERS

    def __init__(self):
        self.params = {}

    def withKeyAs(self, key, op, val):
        """
        :param key: key of doc
        :param val: val that doc.key should have ...
        :param op: ... according to this operator. Must be an instance of
        MongoFilters
        :return: void, saves params
        """

        if not isinstance(op, MongoFilters):
            raise ValueError(self.NOT_VALID_OPERATOR_FORMAT.format(op))

        op = op.value  # get value from enum
        mongo_operator = '${}'.format(op)
        self.params[key] = {
            mongo_operator: val
        }
        return self

    def build(self):
        return MongoQuery(self.params)


class CollectionQueryBuilder(QueryBuilder):
    """ Builds query for exactly this collection. Performs necessary checks.
    ~Proxy pattern """

    INVALID_KEY_FORMAT = 'Cannot find {} in schema of {} of {} database'

    def __init__(self, mongo_client, db_name, collection_name):
        super().__init__()

        self._db_name = db_name
        self._collection_name = collection_name
        self.driver = mongo_client[self._db_name][self._collection_name]

    def raise_key_not_found(self, key):
        message = self.INVALID_KEY_FORMAT.format(
            key,
            self._collection_name,
            self._db_name
        )
        raise ValueError(message)

    def withKeyAs(self, key, op, val):
        """
        :param key: key of doc
        :param val: val that doc.key should have ...
        :param op: ... according to this operator
        :return: Assuming all docs in collection shares same schema, before
        saving params, it checks if key is actually in schema.
        """

        a_random_doc = self.driver.find_one()
        if a_random_doc:  # there is at least one doc
            if key not in a_random_doc:
                self.raise_key_not_found(key)

        return super().withKeyAs(key, op, val)


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

        return self.driver.find(self.params)

    def execute(self, driver=None):
        if driver:
            self.set_driver(driver)

        return self._get_results()
