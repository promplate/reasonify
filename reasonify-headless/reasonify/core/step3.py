from functools import partial
from typing import Any, NotRequired, TypedDict, cast

from promplate import Jump, Node
from promplate.chain.utils import resolve

from ..models.tool import Tool
from ..utils.context import Context, new_checkpoint
from ..utils.globals import DotTemplate as Template
from ..utils.resolve import root

(
    step3 := Node(
        Template.read(root / "step3.j2"),
        response_format={"type": "json_object"},
        temperature=0,
    )
).add_pre_processes(partial(new_checkpoint, name="step3"))


class Action(TypedDict):
    purpose: str
    tool_id: str
    payload: dict
    result: NotRequired[Any]
    tool: NotRequired[Tool]


class Step3Schema(TypedDict):
    note: str
    actions: list[Action]

    # from parents
    tools: list[Tool]


@step3.mid_process
def parse(context):
    c = Context(context)
    parsed = c.extract_json({}, Step3Schema)

    c.update(parsed)


@step3.end_process
async def run_tools(context):
    c = cast(Step3Schema, Context(context))
    if not c["actions"]:
        raise Jump(step3)  # fail to generate actions

    for action in c["actions"]:
        for tool in cast(list[Tool], c["tools"]):
            if tool["id"] == action["tool_id"]:
                action["tool"] = tool
                action["result"] = await resolve(tool["run"](**action["payload"]))
