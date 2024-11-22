from asyncio import iscoroutinefunction
from inspect import Signature, isasyncgenfunction
from typing import Callable

from promplate_recipes.functional.component import SimpleComponent

from .component import register_component
from .run import get_context


def tool[T: Callable](function: T) -> T:
    get_context()[function.__name__] = function

    prefix = "async def" if isasyncgenfunction(function) or iscoroutinefunction(function) else "def"

    stubs[function.__name__] = f'{prefix} {function.__name__}{Signature.from_callable(function, eval_str=True)}:\n    """{function.__doc__}"""'

    return function


stubs = {}


@register_component("stubs")
@SimpleComponent
def stubfile():
    return f"```py\n{"\n\n".join(stubs.values())}\n```"


@tool
def reply(*_):
    """placeholder for examples to be runnable"""


@tool
def end_of_turn():
    """placeholder for examples to be runnable"""
