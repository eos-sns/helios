# -*- coding: utf-8 -*-

import abc

from helios.models.mongo.config import MongoFilters


class CoupleOperators(abc.ABC):
    def __init__(self, available=None):
        self.available = available

    def get_val(self, operator):
        if operator in self.available:
            return self.available[operator]

        return None

    def evaluate(self, operator, pair):
        lambda_f = self.available[operator]
        return lambda_f(pair)


class MongoOperators(CoupleOperators):
    """ Operators -> function when dealing with pair of numbers """

    OPERATORS = {
        'eq': lambda x: x[0] == x[1],
        'ne': lambda x: x[0] != x[1],
        'gte': lambda x: x[0] >= x[1],
        'gt': lambda x: x[0] > x[1],
        'lte': lambda x: x[0] <= x[1],
        'lt': lambda x: x[0] < x[1]
    }

    def __init__(self):
        super().__init__(self.OPERATORS)


class ArithmeticOperators(CoupleOperators):
    """ Operators -> function when dealing with pair of numbers """

    OPERATORS = {
        '==': lambda x: x[0] == x[1],
        '!=': lambda x: x[0] != x[1],
        '>=': lambda x: x[0] >= x[1],
        '>': lambda x: x[0] > x[1],
        '<=': lambda x: x[0] <= x[1],
        '<': lambda x: x[0] < x[1]
    }

    def __init__(self):
        super().__init__(self.OPERATORS)


class ArithmeticToMongoOperators(CoupleOperators):
    """ Operators -> function when dealing with pair of numbers """

    OPERATORS = {
        '==': MongoFilters.EQUALS,
        '!=': MongoFilters.NOT_EQUALS,
        '<': MongoFilters.LESS_THAN,
        '<=': MongoFilters.LESS_THAN_OR_EQUAL_TO,
        '>': MongoFilters.GREATER_THAN,
        '>=': MongoFilters.GREATER_THAN_OR_EQUAL_TO,
    }

    def __init__(self):
        super().__init__(self.OPERATORS)
