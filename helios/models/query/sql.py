# -*- coding: utf-8 -*-

import re

from models.query.eos import EosQuery
from models.query.mongo import MongoFilters, MongoQueryBuilder


class SqlOperation:
    def __init__(self, param, operation, val):
        self.param = param
        self.operation = operation
        self.val = val

        self._parse()

    def _parse(self):
        self.param = self.param.strip()
        if isinstance(self.val, str):
            self.val = self.val.strip()
            self.val = float(self.val)

        self.operation = self.operation.strip()
        self.operation = self._translate_operator(self.operation)

    @staticmethod
    def _translate_operator(op):
        op_to_mongo = {
            '==': MongoFilters.EQUALS,
            '!=': MongoFilters.NOT_EQUALS,
            '<': MongoFilters.LESS_THAN,
            '<=': MongoFilters.LESS_THAN_OR_EQUAL_TO,
            '>': MongoFilters.GREATER_THAN,
            '>=': MongoFilters.GREATER_THAN_OR_EQUAL_TO,
        }

        if op in op_to_mongo:
            return op_to_mongo[op]

        return None


class SqlQueryAdapter:
    """ Adapter for SQL queries working with QueryBuilder """

    def __init__(self, mongo_adaptee=MongoQueryBuilder):
        """
        :param mongo_adaptee: Class of adaptee builder for MongoDB query
        """

        self.mongo_builder = mongo_adaptee()

    def _parse(self, raw_sql):
        def _parse_operation(operation):
            # todo add start, end of string regex
            operators = ['<', '<=', '>', '>=', '==', '!=']
            operators_regex = '|'.join(op for op in operators)
            param_regex = '\w+'
            numbers_regex = '[-\+]?(\d+\.\d+|\d+)'  # float and int, - and +
            matches_regex = ''
            matches_regex += '(?P<param>{})'.format(param_regex)
            matches_regex += '(?P<op>{})'.format(operators_regex)
            matches_regex += '(?P<num>{})'.format(numbers_regex)
            matches_regex = re.compile(matches_regex)
            match = matches_regex.search(operation.replace(' ', ''))
            return SqlOperation(*match.group('param', 'op', 'num'))

        def _parse_sentence(sentence):
            operators = ['and']  # used to concatenate operations
            operators_regex = '|'.join((' ' + op + ' ') for op in operators)
            operators_regex = re.compile(operators_regex)
            operations = operators_regex.split(sentence)
            return [_parse_operation(op) for op in operations]

        parsed = _parse_sentence(raw_sql)
        for sql_operation in parsed:
            self.mongo_builder.set_key_as(
                sql_operation.param,
                sql_operation.operation,
                sql_operation.val
            )

    def build(self, raw_sql):
        self._parse(raw_sql)
        return self.mongo_builder.build(query_class=EosQuery)
