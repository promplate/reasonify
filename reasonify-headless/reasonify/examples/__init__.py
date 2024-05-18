from pathlib import Path

from yaml import CLoader, load

from ..models.shot import Shot


def parse_shot(file: Path):
    return Shot(title=file.stem, interactions=load(file.read_text(), CLoader))


async def get_examples():
    return sum([await parse_shot(file).get_messages() for file in Path(__file__).parent.glob("*.yaml")], [])
