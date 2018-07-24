from pymongo import MongoClient
from django.conf import settings


class MongoConnectionBase(object):
    _connections = {}

    def __init__(self):
        for key in settings.MONGO_DATABASES:
            config = settings.MONGO_DATABASES[key]
            host = config['host']
            port = int(config['port'])
            key = config['host'] + ":" + config['port']
            if key not in self._connections.keys():
                self._connections[key] = MongoClient(host=host, port=port, connect=False)

    def get_connection(self, host, port):
        key = host + port
        if key not in self._connections.keys():
            self._connections[key] = MongoClient(host=host, port=int(port), connect=False)
        return self._connections[key]


mongo_connector = MongoConnectionBase()
