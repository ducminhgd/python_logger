# coding=utf-8
import json
from logging.handlers import HTTPHandler

import requests

from common.utils import format_stack_trace, ExtendedJsonEncoder


class PersistentHTTPHandler(HTTPHandler):
    def __init__(self, logPath, host, url, method):
        HTTPHandler.__init__(self, host, url, method)
        self.logPath = logPath
        self.s = requests.Session()

    def mapLogRecord(self, record):
        record_modified = HTTPHandler.mapLogRecord(self, record)
        record_modified['logPath'] = self.logPath
        try:
            record_modified['msg'] = self.format(record)
        except:
            pass
        return record_modified

    def emit(self, record):
        try:
            host = self.host
            url = self.url
            url = 'http://' + host + '/' + url
            data = self.mapLogRecord(record)
            self.s.post(url, data=data, timeout=10)

        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)


class MongoHTTPHandler(HTTPHandler):
    def __init__(self, db_host, db_port, db_name, collection, host, url, method):
        HTTPHandler.__init__(self, host, url, method)
        self.db_host = db_host
        self.db_port = db_port
        self.db_name = db_name
        self.collection = collection
        self.s = requests.Session()

    def mapLogRecord(self, record):
        record_modified = HTTPHandler.mapLogRecord(self, record)
        try:
            record_modified['msg'] = self.format(record)
        except:
            pass
        record_modified['exc_info'] = format_stack_trace(record_modified['exc_info'])
        record_modified['args'] = str(record_modified['args'])
        return record_modified

    def emit(self, record):
        try:
            host = self.host
            url = self.url
            url = 'http://' + host + '/' + url
            data = self.mapLogRecord(record)
            json_data = {
                'db_host': self.db_host,
                'db_port': self.db_port,
                'db_name': self.db_name,
                'collection': self.collection,
                'data': data,
            }
            json_data = json.dumps(json_data, cls=ExtendedJsonEncoder)
            self.s.post(url, json=json_data, timeout=10)

        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)
