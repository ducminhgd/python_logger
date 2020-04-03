from logging import Handler, INFO
import json
import requests


class LogTelegramHandler(Handler):
    """Log Handler send messages to telegram

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
    """

    def __init__(self, token, chat_id, parse_mode='markdown', level=INFO):
        super().__init__(level=level)
        self.token = token
        self.chat_id = chat_id
        self.parse_mode = parse_mode
        self.send_webhook = 'https://api.telegram.org/bot{token}/sendMessage'.format(token=self.token)
        self.session = requests.Session()

    def emit(self, record):
        try:
            message = self.format(record)
            data = {
                'chat_id': self.chat_id,
                'text': message,
                'parse_mode': self.parse_mode
            }
            self.session.post(self.send_webhook, data=data, timeout=10)
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)