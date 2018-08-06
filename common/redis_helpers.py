# coding=utf-8
"""This module is a helper for Redis"""

import redis
import os
from importlib import import_module


class NullSettings(object):
    pass


class RedisHelper(object):
    _connections = {}
    settings = None

    def __init__(self):
        if os.environ.get('DJANGO_SETTINGS_MODULE', None) is not None:
            from django.conf import settings
            self.settings = settings
        elif os.environ.get('SETTINGS_MODULE', None) is not None:
            self.settings = import_module(os.environ.get('SETTINGS_MODULE'))
        else:
            self.settings = NullSettings()

        if not hasattr(self.settings, 'REDIS'):
            setattr(self.settings, 'REDIS', {})

    def connect(self, config_key, config_dict=None):
        if not isinstance(config_dict, dict):
            if config_key not in self.settings.REDIS:
                return False
            else:
                config_dict = self.settings.REDIS[config_key]

        options = config_dict.get('OPTIONS', None)
        if not isinstance(options, dict):
            options = {}
        max_connections = options.get('MAX_CONNECTION', 100)
        socket_path = config_dict.get('SOCKET_PATH', None)
        host = config_dict.get('HOST', '127.0.0.1')
        port = config_dict.get('PORT', 6379)
        db = config_dict.get('DB', 0)
        self._connections[config_key] = redis.Redis(
            host=host, port=port, db=db, unix_socket_path=socket_path,
            max_connections=max_connections,
            ssl_keyfile=options.get('SSL_KEYFILE', None),
            ssl_certfile=options.get('SSL_CERTFILE', None),
            ssl_cert_reqs=options.get('SSL_CERT_REQS', None),
            ssl_ca_certs=options.get('SSL_CA_CERTS', None),
            ssl=options.get('SSL', False)
        )
        return self._connections[config_key]

    def get_connection(self, config_key):
        if not self.is_connected(config_key):
            self.connect(config_key)
        return self._connections[config_key]

    def get_connections(self):
        for key, config in self.settings.REDIS.items():
            self.get_connection(key)
        return self._connections

    def is_connected(self, config_key):
        if config_key not in self._connections:
            return False
        return self._connections is not None


redis_helper = RedisHelper()
REDIS_CONNECTIONS = redis_helper.get_connections()
