# -*- coding: utf-8 -*-

from models.query.eos import EosQuery
from models.query.mongo import MongoQueryBuilder
from models.sql.query import SqlParser


class SqlQueryAdapter:
    """ Adapter for SQL queries working with QueryBuilder """

    def __init__(self, mongo_adaptee=MongoQueryBuilder):
        """
        :param mongo_adaptee: Class of adaptee builder for MongoDB query
        """

        self.mongo_builder = mongo_adaptee()

    def _parse(self, raw_sql):
        operations = SqlParser(raw_sql).params
        for sql_operation in operations:
            self.mongo_builder.set_key_as(
                sql_operation.param,
                sql_operation.operation,
                sql_operation.val
            )

    def build(self, raw_sql):
        self._parse(raw_sql)
        return self.mongo_builder.build(query_class=EosQuery)
