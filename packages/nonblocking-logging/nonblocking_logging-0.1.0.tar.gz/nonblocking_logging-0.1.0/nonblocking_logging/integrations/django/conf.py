"""
Settings for logging are all namespaced in the NONBLOCKING_LOGGING_LISTENERS setting.
For example your project's settings might look like this:

NONBLOCKING_LOGGING_LISTENERS = {
    'LISTENER_#1': {
        'HANDLER_CLASSES': [
            {
                'class': 'nonblocking_logging.handlers.TelegramQueueHandler',
                'level': 'ERROR',
                'bot_token': TELEGRAM_BOT_TOKEN,
                'chat_id': TELEGRAM_LOGGING_CHAT,
            },
        ],
        'QUEUE_OBJECT': <REFERENCE_ON_EXISTING_Q_OBJECT>,
        'RESPECT_HANDLER_LEVEL': True,
    },
    'LISTENER_#2': [
        'HANDLER_CLASSES': [
            {
                'class': 'nonblocking_logging.handlers.TelegramQueueHandler',
                'level': 'ERROR',
                'bot_token': TELEGRAM_BOT_TOKEN_#2,
                'chat_id': TELEGRAM_LOGGING_CHAT_#2,
            },
        ],
        'QUEUE_OBJECT': <REFERENCE_ON_EXISTING_Q_OBJECT_#2>,
        'RESPECT_HANDLER_LEVEL': True,
    ],
}
"""
from logging.handlers import QueueListener

from django.conf import settings as django_settings
from django.utils.module_loading import import_string


def init_listeners():
    # TODO: rewrite, make readable)
    listener_settings = getattr(django_settings, 'NONBLOCKING_LOGGING_LISTENERS', {})

    listeners = []

    for listener_name, listener_config in listener_settings.items():
        queue_object = listener_config['QUEUE_OBJECT']
        respect_handler_level = listener_config['RESPECT_HANDLER_LEVEL']
        handler_classes = listener_config['HANDLER_CLASSES']
        handlers = []

        for handler_class in handler_classes:
            class_name = handler_class.pop('class', None)
            handler = import_string(class_name)(**handler_class)
            handlers.append(handler)

        listeners.append(QueueListener(
            queue_object,
            *handlers,
            respect_handler_level=respect_handler_level
        ))

    return listeners
