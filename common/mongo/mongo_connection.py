from pymongo import MongoClient

class MongoConnectionBase(object):
    _connections = {}

    def get_connection(self, host, port):
        if host is None or port is None:
            return None
        key = host + ":" + port
        if key not in self._connections.keys():
            self._connections[key] = MongoClient(host=host, port=int(port), connect=False)
        return self._connections[key]


mongo_connector = MongoConnectionBase()
