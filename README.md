# Python logger


## Sample configuration

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
    },
    'loggers': {
        'test_logger': {
            'handlers': ['test'],
            'level': 'INFO',
            'propagate': True,
        },
    }
}
```

## Sample Log Hanlder

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
        record_modified['msg'] = record_modified['msg'].encode('utf-8')
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