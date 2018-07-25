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
        'slack_notification': {
            'level': 'ERROR',
            'class': 'demo_hanlders.LogSlackHandler',
            'webhook': 'Slack web hook',
            'sender': 'System name or Host name',
            'channel': '#slack-notification',
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

## Sample Log Handler

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

## Using handlers

### Telegram Handler

[Telegram Bot API](https://core.telegram.org/bots/api)

1. Register bot:
    - Login Telegram
    - Search for `BotFather` with **verify sign**.
    - Follow `BotFather`'s instructions to register a bot.
    - Bot's token is like this `111111111:AxxxxxxxxxxxxxxxxxxxxxxxxE`
2. Find `chat_id`:
    - Add your bot to group chat and set it as an admin
    - Call POST to URL `https://api.telegram.org/bot<token>/getUpdates`, you will get result like

        ```javascript
        {
            "ok": true,
            "result": [
                {
                    "update_id": 879273682,
                    "message": {
                        "message_id": 1,
                        "from": {
                            ...
                        },
                        "chat": {
                            "id": -222222,
                            "title": "Group name",
                            "type": "supergroup"
                        },
                        "date": 1585919398,
                        "migrate_from_chat_id": -33333
                    }
                }
            ]
        }
        ```

    - Group chat id is `result.message.chat.id`, the negative number `-222222`.
3. Configure handler like this example:

    ```python
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'test_telegram': {
                'class': 'handlers.telegram_handler.LogTelegramHandler',
                'token': '<your_token>',
                'chat_id': '<your_chat_id>'
            },
        },
        'loggers': {
            'test_logger': {
                'handlers': ['test_telegram'],
                'level': 'INFO',
                'propagate': True,
            },
        }
    }
    ```
