# coding=utf-8
import json
import logging
import socket

from common import utils
from common.redis_helpers import redis_helper


class RedisHandler(logging.Handler):
    """
    Redis Handler
    """
    _connection = None
    _sender = None
    _log_level_keys = {
        logging.CRITICAL: '{sender}:CRITICAL',
        logging.ERROR: '{sender}:ERROR',
        logging.WARNING: '{sender}:WARNING',
        logging.INFO: '{sender}:INFO',
        logging.DEBUG: '{sender}:DEBUG',
        logging.NOTSET: '{sender}:NOTSET',
    }
    _log_all_key = '{sender}:LOG'

    def __init__(self, level=logging.INFO, sender=None, host='127.0.0.1', port=6379, db=0, options=None):
        logging.Handler.__init__(self)
        config_dict = {
            'HOST': host,
            'PORT': int(port),
            'DB': db,
            'OPTIONS': options or {},
        }

        # Get sender's name
        if sender is None:
            sender = socket.gethostname()
        self._sender = sender

        # Parsing keys
        for key, value in self._log_level_keys.items():
            self._log_level_keys[key] = value.format(sender=sender)
        self._log_all_key = self._log_all_key.format(sender=sender)

        self._connection = redis_helper.connect(sender, config_dict)

    def mapLogRecord(self, record):
        """
        Map log record in to required format
        :param record:
        :return:
        """
        record.msg = self.format(record)
        return record.__dict__

    def emit(self, record):
        """
        Emit log
        :param record:
        :return:
        """
        try:
            dict_data = self.mapLogRecord(record)
            json_data = json.dumps(dict_data, cls=utils.ExtendedJsonEncoder)
            self._connection.rpush(self._log_all_key, json_data)
            self._connection.rpush(self._log_level_keys[dict_data['levelno']], json_data)
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)


if __name__ == '__main__':
    from logging import config

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': True,
        'formatters': {
            'verbose': {
                'format': '%(levelname)s | %(process)d | %(thread)d | %(asctime)s | %(filename)s:%(lineno)d | %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S',
            },
            'simple': {
                'format': '%(message)s'
            },
        },
        'handlers': {
            'test': {
                'formatter': 'simple',
                'level': 'INFO',
                'class': 'handlers.redis_handler.RedisHandler',
                'sender': None,
                'host': '127.0.0.1',
                'port': 6379,
                'db': 1,
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
    logger = logging.getLogger('test_logger')
    try:
        a = 1 / 0
    except:
        logger.error('error')
