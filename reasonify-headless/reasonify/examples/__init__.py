from pathlib import Path

from yaml import CLoader, load

from ..models.shot import Shot
from ..utils.tool import tool


def parse_shot(file: Path):
    return Shot(title=file.stem, interactions=load(file.read_text(), CLoader))


async def get_examples():
    # dummy tools for running few-shot examples:
    @tool
    def reply(*_): ...
    @tool
    def end_of_turn(): ...

    return sum([await parse_shot(file).get_messages() for file in Path(__file__).parent.glob("*.yaml")], [])
