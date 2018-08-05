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
            'url': 'http-daily-logger/',
            'host': 'localhost:1234',
            'method': 'POST',
            'logPath': '/tmp/python_logger/log'
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
        }
    },
    'loggers': {
        'test_logger': {
            'handlers': ['test_mongo'],
            'level': 'INFO',
            'propagate': True,
        },
    }
}

logging.config.dictConfig(LOGGING)

if __name__ == '__main__':
    logger = logging.getLogger('test_logger')
    try:
        a = 1 / 0
    except:
        logger.exception('error')
    # start = time.time()
    # for i in range(0, 1):
    #     logger.info('1' * 100)
    #
    # print(time.time() - start)
