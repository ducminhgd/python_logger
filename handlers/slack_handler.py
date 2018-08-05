# coding=utf-8
import json
import socket
from logging import Handler, INFO

import requests


class LogSlackHandler(Handler):
    """
    Log handler
    """
    __color_dict = {
        'INFO': 'info',
        'WARNING': 'warning',
        'WARN': 'warning',
        'ERROR': 'danger',
    }

    def __init__(self, level=INFO, webhook='', username='LogSlackHandler bot',
                 icon_emoji=':loud_sound:', sender=None, channel='#slack-notification'):
        """
        Constructor
        :param level: log level
        :param webhook: Slack webhook
        :param username: display Username of bot
        :param icon_emoji: icon for bot
        :param sender: send from whom
        :param channel: channel to send
        """
        Handler.__init__(self, level)
        self.webhook = webhook
        self.username = username
        self.icon_emoji = icon_emoji
        if sender is None:
            sender = socket.gethostname()
        self.sender = sender
        self.channel = channel
        self.session = requests.Session()

    def mapLogRecord(self, record):
        """
        Map log record in to required format
        :param record:
        :return:
        """
        pretext = '*<!channel> {level}*'.format(level=record.levelname)
        title = '[{level}] - {sender}'.format(level=record.levelname, sender=self.sender)
        message = self.format(record)

        payload = {
            'username': self.username,
            'icon_emoji': self.icon_emoji,
            'channel': self.channel,
            'attachments': [
                {
                    'pretext': pretext,
                    'color': self.__color_dict.get(record.levelname, 'INFO'),
                    'mrkdwn_in': [
                        'pretext'
                    ],
                    'fields': [
                        {
                            'title': title,
                            'value': message,
                            'short': False
                        }
                    ]
                }
            ]
        }
        payload = json.dumps(payload)
        return payload

    def emit(self, record):
        """
        Emit log
        :param record:
        :return:
        """
        try:
            data = self.mapLogRecord(record)
            self.session.post(self.webhook, data=data, timeout=10)
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)
