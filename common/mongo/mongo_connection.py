from pymongo import MongoClient


class MongoConnection(object):
    def __init__(self, db):
        name = db['name']
        host = db['host']
        port = int(db['port'])
        if name is None or host is None or port is None:
            return
        client = MongoClient(host=host, port=port)
        self.db = client[name]

    def get_collection(self, name):
        self.collection = self.db[name]
