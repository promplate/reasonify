from typing import Callable, TypedDict


class Tool(TypedDict):
    id: str
    name: str
    usage: str
    schema: str
    instruction: str
    run: Callable
