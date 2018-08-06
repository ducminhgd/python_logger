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
    _root_key = None
    _log_level_keys = {
        logging.CRITICAL: '{root_key}:CRITICAL',
        logging.ERROR: '{root_key}:ERROR',
        logging.WARNING: '{root_key}:WARNING',
        logging.INFO: '{root_key}:INFO',
        logging.DEBUG: '{root_key}:DEBUG',
        logging.NOTSET: '{root_key}:NOTSET',
    }
    _log_all_key = '{root_key}:LOG'
    _write_log_all = True

    def __init__(self, root_key=None, host='127.0.0.1', port=6379, db=0, options=None):
        logging.Handler.__init__(self)
        config_dict = {
            'HOST': host,
            'PORT': int(port),
            'DB': db,
            'OPTIONS': options or {},
        }
        connection_url = '{host}:{port}/{db}'.format(host=host, port=port, db=db)

        self._write_log_all = options.get('all', True)

        # Get root_key's name
        if root_key is None:
            root_key = socket.gethostname()
        self._root_key = root_key

        # Parsing keys
        for key, value in self._log_level_keys.items():
            self._log_level_keys[key] = value.format(root_key=root_key)
        self._log_all_key = self._log_all_key.format(root_key=root_key)

        self._connection = redis_helper.connect(connection_url, config_dict)

    def mapLogRecord(self, record):
        """
        Map log record in to required format
        :param record:
        :return:
        """
        self.format(record)
        record.exc_info = record.exc_text
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
            if self._write_log_all:
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
                'root_key': None,
                'host': '127.0.0.1',
                'port': 6379,
                'db': 1,
                'options': {
                    'all': False,
                },
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
        d = {
            'a': 1,
            'b': 2,
        }
        logger.exception(d)
