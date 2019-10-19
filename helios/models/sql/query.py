# -*- coding: utf-8 -*-

import re

from helios.models.operators import ArithmeticToMongoOperators


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
        self.operation = ArithmeticToMongoOperators().get_val(self.operation)

    @staticmethod
    def from_raw(operation):
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


class SqlParser:
    """ Parses SQL-like """

    def __init__(self, raw):
        self.raw = raw
        self.params = self._parse_sentence(self.raw)

    @staticmethod
    def _parse_sentence(sentence, operators=None):
        if operators is None:
            operators = ['and']

        operators_regex = '|'.join((' ' + op + ' ') for op in operators)
        operators_regex = re.compile(operators_regex)
        operations = operators_regex.split(sentence)
        return [SqlOperation.from_raw(op) for op in operations]
