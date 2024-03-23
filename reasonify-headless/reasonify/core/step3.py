from typing import Any, Callable, NotRequired, TypedDict, cast

from box import BoxList
from promplate import Node, Template

from ..utils.context import Context, new_checkpoint
from ..utils.globals import make_context
from ..utils.resolve import root

(
    step3 := Node(
        Template.read(root / "step3.j2"),
        make_context(),
        response_format={"type": "json_object"},
        temperature=0,
    )
).add_pre_processes(new_checkpoint)


class Tool(TypedDict, total=False):
    id: str
    name: str
    usage: str
    schema: str
    instruction: str
    run: Callable


class Action(TypedDict):
    purpose: str
    tool_id: str
    payload: dict
    result: NotRequired[Any]
    tool: NotRequired[Tool]


class Step3Schema(TypedDict):
    note: str
    actions: list[Action]


@step3.mid_process
def parse(context):
    c = Context(context)
    parsed = c.extract_json({}, Step3Schema)

    c.update(parsed)


@step3.end_process
def run_tools(context):
    c = cast(Step3Schema, Context(context))
    for action in c["actions"]:
        for tool in cast(list[Tool], c["tools"]):
            if tool["id"] == action["tool_id"]:
                action["tool"] = tool
                action["result"] = tool["run"](**action["payload"])

    c["actions"] = BoxList(c["actions"])
