from asyncio import Queue
from contextlib import contextmanager
from contextvars import ContextVar
from typing import Literal


def create_event_queue():
    q = Queue[Literal[0, 1]]()

    @contextmanager
    def event_listener():
        _event_handler.set(lambda: q.put_nowait(1))
        try:
            yield
        finally:
            q.put_nowait(0)

    return event_listener, lambda: q.get()


_event_handler = ContextVar("event-handler", default=lambda: None)


def trigger_event():
    _event_handler.get()()


__all__ = ("create_event_queue", "trigger_event")
