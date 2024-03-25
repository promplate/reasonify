from contextlib import suppress
from functools import partial
from typing import Literal, NotRequired, TypedDict

from promplate import Chain, Jump, Node

from ..utils.context import Context, new_checkpoint
from ..utils.globals import DotTemplate as Template
from ..utils.resolve import root

step4a = Node(Template.read(root / "step4a.j2"))
step4b = Node(Template.read(root / "step4b.j2"), response_format={"type": "json_object"})


class NextStep(TypedDict):
    plan: str
    tools: list[str]


class Step4Schema(TypedDict):
    action: Literal["finish", "continue"]
    message: NotRequired[str]
    next_step: NotRequired[NextStep]

    summary: NotRequired[str]


(step4 := step4a + step4b).add_pre_processes(partial(new_checkpoint, name="step4"))


@step4a.mid_process
def _(context):
    c = Context(context)
    c["summary"] = c.result


@step4b.mid_process
def parse(context):
    c = Context(context)
    with suppress(SyntaxError, KeyError):
        parsed = c.extract_json({}, Step4Schema)
        c["action"] = parsed["action"]
        c.update(parsed)


@step4.end_process
def router(context):
    c = Context(context)

    if c.get("action") == "continue":
        from . import step2, step3

        raise Jump(Chain(step2, step3, step4))
