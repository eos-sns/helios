# -*- coding: utf-8 -*-


class CoupleOperators:
    def __init__(self, available):
        self.available = available

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
