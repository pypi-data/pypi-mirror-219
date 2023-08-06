from .conf import init_listeners


def start_queue_listening():
    listeners = init_listeners()

    for listener in listeners:
        listener.start()
