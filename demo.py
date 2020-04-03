# -*- coding: utf-8 -*-
import logging.config
import time

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'test': {
            'level': 'INFO',
            'class': 'handlers.http_handler.PersistentHTTPHandler',
            'formatter': 'verbose',
            'url': 'http-daily-logger/',
            'host': 'localhost:1234',
            'method': 'POST',
            'log_path': '/tmp/python_logger/log',
            'day': 20    # keep logs changed within n days
        },
        'test_mongo': {
            'level': 'INFO',
            'class': 'handlers.http_handler.MongoHTTPHandler',
            'url': 'http-mongo-logger/',
            'host': 'localhost:1234',
            'method': 'POST',
            'db_host': '127.0.0.1',
            'db_port': '27017',
            'db_name': 'logs',
            'collection': 'logs',
        },
        'test_telegram': {
            'class': 'handlers.telegram_handler.LogTelegramHandler',
            'token': '<token>',
            'chat_id': '<chat_id>'
        },
    },
    'loggers': {
        'test_logger': {
            'handlers': ['test_telegram'],
            'level': 'INFO',
            'propagate': True,
        },
    },
    'formatters': {
        'verbose': {
            'format': '%(asctime)s | %(levelname)s | %(process)d | %(thread)d | %(filename)s:%('
                      'lineno)d | %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        'simple': {
            'format': '%(levelname)s | %(message)s'
        },
    },
}

logging.config.dictConfig(LOGGING)

if __name__ == '__main__':
    logger = logging.getLogger('test_logger')
    try:
        a = 1 / 0
    except:
        logger.exception('*ZeroDivision error*')
