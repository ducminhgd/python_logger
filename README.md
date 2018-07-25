# Python logger


## Sample configuration

### Client Side
```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'test': {
            'level': 'INFO',
            'class': 'demo_hanlders.PersistentHTTPHandler',
            'url': 'http-daily-logger/',
            'host': 'localhost:1234',
            'method': 'POST',
            'logPath': '/tmp/python_logger/log'
        },
        'test_mongo': {
            'level': 'INFO',
            'class': 'demo_handlers.MongoHTTPHandler',
            'url': 'http-mongo-logger/',
            'host': 'localhost:1234',
            'method': 'POST',
            'db_host': '127.0.0.1',
            'db_port': '27017',
            'db_name': 'logs',
            'collection': 'logs',
        }
    },
    'loggers': {
        'test_logger': {
            'handlers': ['test', 'test_mongo'],
            'level': 'INFO',
            'propagate': True,
        },
    }
}
```

## Sample Log Hanlder

### File HTTP Handler

```python
import requests
from logging.handlers import HTTPHandler

class PersistentHTTPHandler(HTTPHandler):
    def __init__(self, logPath, host, url, method):
        HTTPHandler.__init__(self, host, url, method)
        self.logPath = logPath
        self.s = requests.Session()

    def mapLogRecord(self, record):
        record_modified = HTTPHandler.mapLogRecord(self, record)
        record_modified['logPath'] = self.logPath
        record_modified['msg'] = (record_modified['msg'] % record_modified['args']).encode('utf-8')
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
```

### Mongo HTTP Handler

```python
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
```

## Run

### With Gunicorn

```bash
gunicorn python_logger.wsgi:application -k gevent -w 4 -b 127.0.0.1:1234 --log-file /var/log/python_logger/gunicorn.log --keep-alive 5 --graceful-timeout 60 --pid /tmp/python-logger.pid
```

### With SystemD

```bash
# python_logger.service
[Unit]
Description=python_logger
After=network.target

[Service]
PIDFile=/tmp/python_logger.pid
User=root
Group=root
WorkingDirectory=/data/python_logger
ExecStart=/data/python_logger/.venv/bin/gunicorn python_logger.wsgi:application -k gevent -w 4 -b 127.0.0.1:1234 --log-file /var/log/python_logger/gunicorn.log --keep-alive 5 --graceful-timeout 60 --pid /tmp/python-logger.pid
ExecReload = /bin/kill -s HUP $MAINPID
ExecStop = /bin/kill -s TERM $MAINPID
Restart=always

[Install]
WantedBy=multi-user.target
```

## Contributors

- ducminhgd
- vchitai