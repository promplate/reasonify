from inspect import getsource
from textwrap import dedent
from typing import Callable

from promplate_recipes.functional.component import SimpleComponent

from .component import register_component
from .run import get_context


def tool[T: Callable](function: T) -> T:
    get_context()[function.__name__] = function

    source = dedent(getsource(function))

    signature = source[: source.index('"""')]
    docstring = function.__doc__

    stubs[function.__name__] = "\n".join(f'{signature}"""{docstring}"""'.split("\n")[1:])  # exclude the first line `@tool`

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
