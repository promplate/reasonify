from functools import partial
from typing import TypedDict

from promplate import Jump, Node

from ..utils.context import Context, new_checkpoint
from ..utils.globals import DotTemplate as Template
from ..utils.resolve import root

(
    step2 := Node(
        Template.read(root / "step2.j2"),
        response_format={"type": "json_object"},
        temperature=0,
    )
).add_pre_processes(partial(new_checkpoint, name="step2"))


class Step2Schema(TypedDict, total=False):
    plan: str
    tools: list[str]
    direct_response: str


@step2.pre_process
def increase_step_count(context):
    c = Context(context)
    c["step_count"] = c.get("step_count", 0) + 1


@step2.mid_process
def parse(context):
    c = Context(context)
    parsed = c.extract_json({}, Step2Schema)

    c.update(parsed)

    c["tools"] = [tool for tool in c["all_tools"] if tool["id"] in parsed.get("tools", [])]


@step2.end_process
def break_if_direct_response(context: dict):
    if context.get("direct_response"):
        from . import chain

        raise Jump(out_of=chain)

    elif not context.get("tools"):
        raise ValueError("`tools` field is unexpectedly empty!")
