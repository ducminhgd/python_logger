# coding=utf-8
from logging.handlers import HTTPHandler

import requests


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
