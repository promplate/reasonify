from typing import TypedDict

from promplate import Node

from ..utils.context import Context, new_checkpoint
from ..utils.globals import DotTemplate as Template
from ..utils.resolve import root

(
    step2 := Node(
        Template.read(root / "step2.j2"),
        response_format={"type": "json_object"},
        temperature=0,
    )
).add_pre_processes(new_checkpoint)


class Step2Schema(TypedDict):
    plan: str
    tools: list[str]


@step2.pre_process
def increase_step_count(context):
    c = Context(context)
    c["step_count"] = c.get("step_count", 0) + 1


@step2.mid_process
def parse(context):
    c = Context(context)
    parsed = c.extract_json({}, Step2Schema)

    c["tools"] = [tool for tool in c["all_tools"] if tool["id"] in parsed.get("tools", [])]
    c["plan"] = parsed.get("plan", "")


@step2.end_process
def raise_if_empty(context: dict):
    if not context.get("tools"):
        raise ValueError("`tools` field is unexpectedly empty!")
