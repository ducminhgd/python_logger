from common.mongo.mongo_connection import MongoConnection
from django.conf import settings

class LogsCollection(MongoConnection):
    __collection_name__ = 'logs'
    __database__ = settings.MONGO_DATABASES['default']

    def __init__(self):
        super(LogsCollection, self).__init__(self.__database__)
        self.get_collection(self.__collection_name__)

    def insert(self, obj):
        self.collection.insert_one(obj)

    def update(self, obj):
        self.collection.update({"id": obj.id}, obj)

    def remove(self, obj):
        if self.collection.find({'id': obj.id}).count():
            self.collection.delete_one({'id': obj.id})
