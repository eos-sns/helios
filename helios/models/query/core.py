# -*- coding: utf-8 -*-

from models.query.mongo import MongoQueryBuilder


class CollectionMongoQueryBuilder(MongoQueryBuilder):
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

    def with_key_as(self, key, op, val):
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

        return super().with_key_as(key, op, val)
