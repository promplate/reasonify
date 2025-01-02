from asyncio import ensure_future
from json import dumps

from partial_json_parser import Allow
from promplate import Callback, Chain, Jump, Loop, Message, Node
from promplate.prompt.chat import assistant, system, user
from promplate_recipes.functional.node import SimpleNode

from ..examples import get_examples
from ..templates import main
from ..utils.context import Context, new_checkpoint
from ..utils.inject import dispatch_context
from ..utils.queue import QueueWrapper
from ..utils.run import run
from ..utils.serialize import json
from ..utils.tool import tool


@SimpleNode
@dispatch_context
async def intro(c: Context, query: str, messages: list[Message]):
    messages.append(user > query)

    response = c["response"] = []
    c["end"] = False

    @tool
    def reply(*messages: str):
        """talk to the user"""
        response.extend(messages)

    @tool
    def end_of_turn():
        """end this round of conversation and pass the microphone to the user"""
        c["end"] = True


@intro.pre_process
async def _(context: dict):
    if "few_shot" not in context:
        context["few_shot"] = await get_examples()
    context["messages"] = context.get("messages", [])
    new_checkpoint(context)


main_loop = Chain(intro, loop := Loop(main := Node(main)))


@main.callback
class _(Callback):
    async def run_jobs_until_end(self):
        async for source in self._queue:
            self.results.append(await run(source))

    @dispatch_context
    def pre_process(self, c: Context):
        if "sources" not in c:
            c["sources"] = []
        if "results" not in c:
            c["results"] = []

        self._queue = QueueWrapper[str]()
        self._index = self._last = len(c["sources"])
        self._pure_text = False
        self.sources: list[str] = c["sources"]
        self.results: list[dict] = c["results"]
        self.future = ensure_future(self.run_jobs_until_end())

    @dispatch_context
    def mid_process(self, c: Context, response: list[str]):
        if not c.result:  # "" in the first yield
            return

        parsed_sources = c.extract_json(None, list[str])

        if parsed_sources is None:
            if fine_sources := self.sources[self._last : self._index]:
                # malformed json in the end
                c.result = dumps(fine_sources, ensure_ascii=False, indent=2)

            # not json at all
            elif self._pure_text:
                response[-1] = c.result  # update the simple replying
            else:
                response.append(c.result)  # treat it as simple replying
                self._pure_text = True

            return

        # normal cases
        self.sources[self._last :] = parsed_sources

        sources = c.extract_json(None, list[str], ~Allow.STR)
        if sources is not None:
            for source in sources[self._index - self._last :]:
                self._queue.put(source)
                self._index += 1

    @dispatch_context
    async def end_process(self):
        self._queue.end()
        await self.future


@loop.end_process
@dispatch_context
async def _(messages: list[Message], end: bool, sources: list, results: list[dict]):
    if sources:
        messages.append(assistant > json(sources))
        messages.append(system @ "results" > json(results))

    if not end:
        return  # next round

    raise Jump(out_of=main_loop)  # already responded or nothing generated
