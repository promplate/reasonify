from asyncio import ensure_future
from operator import call

from partial_json_parser import Allow
from promplate import Chain, Jump, Loop, Message, Node
from promplate.prompt.chat import assistant, system
from promplate_recipes.functional.node import SimpleNode

from ..examples import get_examples
from ..templates import main
from ..utils.context import Context, new_checkpoint
from ..utils.queue import QueueWrapper
from ..utils.run import get_context, run
from ..utils.serialize import json
from ..utils.tool import tool


@SimpleNode
async def intro(context: dict):
    context["few_shot"] = await get_examples()
    context["response"] = []

    @tool
    def reply(message: str):
        """talk to the user"""
        context["response"] += [message]

    get_context()["reply"] = reply


main_loop = Chain(intro, Loop(main := Node(main)))


@main.pre_process
def _(context):
    new_checkpoint(context)

    c = Context(context)
    c["queue"] = queue = QueueWrapper[str]()
    c["index"] = 0
    c["results"] = []

    @ensure_future
    @call
    async def job():
        async for source in queue:
            result = await run(source)
            c["results"] += [result]

    c["future"] = job


@main.mid_process
def _(context):
    c = Context(context)
    c["sources"] = c.extract_json([])

    queue: QueueWrapper[str] = c["queue"]

    for source in c.extract_json([], list[str], ~Allow.STR)[c["index"] :]:
        queue.put(source)
        c["index"] += 1


@main.end_process
async def _(context):
    c = Context(context)
    c["queue"].end()
    await c["future"]

    messages: list[Message] = c["messages"]

    if "sources" in c:
        messages.append(assistant > json(c["sources"]))
        messages.append(system @ "results" > json(c["results"]))

    del c["future"], c["queue"]

    if c["response"] or not c["sources"]:
        raise Jump(out_of=main_loop)
