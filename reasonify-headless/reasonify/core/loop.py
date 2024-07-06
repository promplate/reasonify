from asyncio import Future, ensure_future
from operator import call

from partial_json_parser import Allow
from promplate import Chain, Jump, Loop, Message, Node
from promplate.prompt.chat import assistant, system, user
from promplate_recipes.functional.node import SimpleNode

from ..examples import get_examples
from ..templates import main
from ..utils.context import Context, new_checkpoint
from ..utils.inject import dispatch_context, inject
from ..utils.queue import QueueWrapper
from ..utils.run import get_context, run
from ..utils.serialize import json
from ..utils.tool import tool


@SimpleNode
@dispatch_context
async def intro(c: Context, query: str, messages: list[Message]):
    messages.append(user > query)

    response = c["response"] = []

    @tool
    def reply(message: str):
        """talk to the user"""
        response.append(message)

    get_context()["reply"] = reply


@intro.pre_process
async def _(context: dict):
    context["few_shot"] = await get_examples()
    context["messages"] = context.get("messages", [])
    new_checkpoint(context)


main_loop = Chain(intro, Loop(main := Node(main)))


@main.pre_process
@dispatch_context
def _(c: Context, queue=inject(lambda: QueueWrapper[str]()), results=inject(lambda: list[dict]())):
    @ensure_future
    @call
    async def job():
        async for source in queue:
            results.append(await run(source))

    c.update({"future": job, "index": 0})


@main.mid_process
@dispatch_context
def _(c: Context, index: int, queue: QueueWrapper[str], response: list[str], pure_text=False):
    c["sources"] = c.extract_json([])

    if pure_text:
        response[-1] = c.result
        return

    sources = c.extract_json(None, list[str], ~Allow.STR)
    if sources is None:
        response.append(c.result)
        return c.update({"pure_text": True})

    for source in sources[index:]:
        queue.put(source)
        c["index"] += 1


@main.end_process
@dispatch_context
async def _(c: Context, queue: QueueWrapper, future: Future, messages: list[Message], response: list, sources: list, results: list):
    queue.end()
    await future

    del c["future"], c["queue"], c["pure_text"]

    if sources:
        messages.append(assistant > json(sources))
        messages.append(system @ "results" > json(results))

    if not response:
        return  # next round

    raise Jump(out_of=main_loop)  # already responded or nothing generated
