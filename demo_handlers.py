import json
import traceback

import requests
from logging.handlers import HTTPHandler


def format_stack_trace(exc_info):
    """
    Format exception info as string
    :param exc_info: exception info
    :return: string
    :example:

    import sys

    try:
        ...
    except:
        exc_info = sys.exc_info()
        print(format_stack_trace(exc_info))
    """
    if exc_info[0] is None:
        return ''
    lines = traceback.format_exception(*exc_info)
    return ''.join(line for line in lines)


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
            self.s.post(url, json=json.dumps(json_data), timeout=10)

        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)