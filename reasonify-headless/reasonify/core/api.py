"""Recommended public API for creating a headless Reasonify agent."""

from asyncio import ensure_future
from typing import TypedDict

from promplate import Context, Message
from promplate.prompt.utils import AutoNaming
from pydantic import TypeAdapter, validate_call

from ..utils.event import create_event_queue
from ..utils.run import Result
from .loop import main_loop


class Input(TypedDict):
    query: str


class Snapshot(TypedDict):
    response: list[str]
    sources: list[str]
    results: list[Result]


class Output(TypedDict):
    messages: list[Message]
    snapshots: list[Snapshot]


validate = TypeAdapter(Output).validate_python


class Agent(AutoNaming):
    def __init__(self, context: Context | None = None):
        self.states = {} if context is None else context

    async def ainvoke(self, context: Input, complete=None, **config):
        self.states |= context
        await main_loop.ainvoke(self.states, complete, **config)
        return validate(self.states)

    async def astream(self, context: Input, generate=None, **config):
        self.states |= context

        event_listener, next_update = create_event_queue()

        async def producer():
            with event_listener():
                async for _ in main_loop.astream(self.states, generate, **config):
                    pass

        ensure_future(producer()).add_done_callback(lambda _: _.exception())

        while await next_update():
            yield validate(self.states)

    @property
    def _messages(self) -> list[Message]:
        return self.states.setdefault("messages", [])

    @validate_call
    def append_message(self, message: Message):
        """Append a message to the agent's message list."""
        self._messages.append(message)
