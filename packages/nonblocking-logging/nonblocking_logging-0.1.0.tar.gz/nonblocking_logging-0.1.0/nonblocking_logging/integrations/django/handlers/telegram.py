import logging

from django.conf import settings
from django.utils.module_loading import import_string
from nonblocking_logging.handlers import TelegramHandler as BaseTelegramHandler


class TelegramHandler(BaseTelegramHandler):
    def __init__(self, bot_token, chat_id, level=logging.NOTSET, reporter_class=None):
        super().__init__(level=level, bot_token=bot_token, chat_id=chat_id)
        self._token = bot_token
        self._chat_id = chat_id
        self.reporter_class = import_string(
            reporter_class or settings.DEFAULT_EXCEPTION_REPORTER
        )

    def send_error_message(self, record: logging.LogRecord):
        try:
            request = record.request  # noqa
            subject = "%s (%s IP)" % (
                record.levelname,
                request.META.get("REMOTE_ADDR", 'unknown IP'),
            )
        except Exception as e:
            subject = "%s: %s" % (record.levelname, e)
            request = None

        if record.exc_info:
            exc_info = record.exc_info
        else:
            exc_info = (None, record.getMessage(), None)

        reporter = self.reporter_class(request, *exc_info)
        html_message = reporter.get_traceback_html()

        self._send_document(subject, html_message)
