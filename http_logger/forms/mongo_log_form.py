# coding: utf-8

from django import forms

from common.mongo.mongo_connection import mongo_connector


class MongoLogJson():
    def __init__(self, data):
        self.data = data

    def is_valid(self):
        return isinstance(self.data, dict)

    def store_db(self):
        host = self.data.get('db_host', '127.0.0.1')
        port = self.data.get('db_port', '27017')
        db_name = self.data.get('db_name', 'logs')
        collection_name = self.data.get('collection', 'logs')
        collection = mongo_connector.get_connection(host=host, port=port)
        collection = collection[db_name][collection_name]
        store_data = self.data.get('data', {})
        collection.insert_one(store_data)
