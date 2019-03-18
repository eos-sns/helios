# -*- coding: utf-8 -*-

from helios.models.operators import ArithmeticOperators, \
    MongoOperators, CoupleOperators
from helios.models.sql.query import SqlParser


class MongoResults:
    def __init__(self, results):
        self.results = results

    def filter_by_sql(self, raw_sentence):
        params = SqlParser(raw_sentence).params
        params = {
            op.param: {
                op.operation.value: op.val
            }
            for op in params
        }
        return self.filter_by_params(params, MongoOperators())

    def filter_by_params(self, params, operators=CoupleOperators()):
        """
        :param params: {} of {}. Each dict is key -> {operation -> val}
        :param operators: list of available operators
        :return: filtered list
        """

        filtered = self.results

        for param, constraint in params.items():
            constraint = list(constraint.items())[0]  # there is only 1
            mongo_operator, val = constraint[0], constraint[1]
            filtered = [
                result
                for result in filtered
                if operators.evaluate(mongo_operator, (result[param], val))
            ]

        return filtered

    def filter_by(self, arg):
        if isinstance(arg, str):
            filtered = self.filter_by_sql(arg)
        elif isinstance(arg, dict):
            filtered = self.filter_by_params(arg, ArithmeticOperators())
        else:
            raise ValueError('Cannot filter by {}'.format(arg))

        return MongoResults(filtered)

    def get(self):
        return self.results

    def __str__(self):
        return str(self.results)
