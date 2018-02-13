# -*- coding: utf-8 -*-
import logging.config
import time
import sys

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

logging.config.dictConfig(LOGGING)

if __name__ == '__main__':
    logger = logging.getLogger('test_logger')
    start = time.time()
    for i in range(0, 1):
        logger.info('1' * 100)
    print(time.time() - start)
