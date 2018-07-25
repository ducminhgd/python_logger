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


class MongoLogForm(forms.Form):
    name = forms.CharField()
    created = forms.CharField()
    levelname = forms.CharField()
    process = forms.CharField()
    thread = forms.CharField()
    filename = forms.CharField()
    lineno = forms.CharField()
    module = forms.CharField()
    funcName = forms.CharField()
    msg = forms.CharField()
    db_host = forms.CharField()
    db_port = forms.CharField()
    db_name = forms.CharField()
    collection = forms.CharField()

    def store_db(self):
        host = self.cleaned_data.get('db_host', '127.0.0.1')
        port = self.cleaned_data.get('db_port', '27017')
        db_name = self.cleaned_data.get('db_name', 'logs')
        collection_name = self.cleaned_data.get('collection', 'logs')

        collection = mongo_connector.get_connection(host=host, port=port)
        collection = collection[db_name][collection_name]
        exclude_field = [
            'db_name',
            'db_host',
            'db_port',
            'collection',
            'logPath',
        ]
        data = self.__dict__['data']
        store_data = {field: data.get(field, '') for field in data.keys() if field not in exclude_field}
        collection.insert_one(store_data)
