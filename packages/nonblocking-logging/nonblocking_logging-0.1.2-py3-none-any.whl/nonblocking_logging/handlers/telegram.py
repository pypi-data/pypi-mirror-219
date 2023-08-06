import logging
from datetime import datetime

import requests


class PseudoFile:
    def __init__(self, name, content):
        self.name = name
        self.content = content

    def read(self):
        return self.content


class TelegramHandler(logging.Handler):
    def __init__(self, bot_token, chat_id, level=logging.NOTSET):
        super().__init__(level=level)
        self._token = bot_token
        self._chat_id = chat_id

    def emit(self, record: logging.LogRecord):
        if record.levelno == logging.ERROR:
            self.send_error_message(record)
        else:
            self.send_notification_message(record)

    def send_error_message(self, record: logging.LogRecord):
        raise NotImplementedError

    def send_notification_message(self, record: logging.LogRecord):
        raise NotImplementedError

    def _send_message(self, message):
        requests.post(
            f'https://api.telegram.org/bot{self._token}/sendMessage',
            data={'chat_id': self._chat_id, 'text': message},
        )

    def _send_document(self, subject, message):
        document_name = '%s.%s.html' % (
            datetime.now().strftime('%Y-%m-%dT%H-%M'),
            logging.getLevelName(self.level)
        )
        # TODO: handle 429, e.g. add rate limiter
        requests.post(
            f'https://api.telegram.org/bot{self._token}/sendDocument',
            data={'chat_id': self._chat_id, 'caption': subject},
            files={'document': PseudoFile(document_name, message)},
        )
