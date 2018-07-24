# coding: utf-8

from django import forms

from common.mongo.mongo_connection import mongo_connector


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
        collection = mongo_connector.get_collection(host=self.cleaned_data['db_host'],
                                                    port=self.cleaned_data['db_port'],
                                                    db_name=self.cleaned_data['db_name'],
                                                    collection=self.cleaned_data['collection'])
        # msg = self.cleaned_data['msg']
        collection.insert_one(self.__dict__['data'])
