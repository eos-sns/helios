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
