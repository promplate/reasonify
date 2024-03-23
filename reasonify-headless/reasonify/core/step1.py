from typing import TypedDict

from promplate import Jump, Node, Template

from ..utils.context import Context, new_checkpoint
from ..utils.globals import make_context
from ..utils.resolve import root

(
    step1 := Node(
        Template.read(root / "step1.j2"),
        make_context(),
        response_format={"type": "json_object"},
        temperature=0,
    )
).add_pre_processes(new_checkpoint)


class Step1Schema(TypedDict, total=False):
    response: str
    tools: list[str]


@step1.mid_process
def parse(context):
    c = Context(context)
    parsed = c.extract_json({}, Step1Schema)

    if "tools" in parsed:
        c["tools"] = [tool for tool in c["all_tools"] if tool["id"] in parsed["tools"]]

    elif "response" in parsed:
        c["response"] = parsed["response"]


@step1.end_process
def break_out(context):
    if "response" in context:
        from . import chain

        raise Jump(out_of=chain)

    elif not context["tools"]:
        raise ValueError("`tools` field is unexpectedly empty!")
