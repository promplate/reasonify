from importlib import import_module
from pathlib import Path


def register_all():
    for file in Path(__file__).parent.glob("*.py"):
        if file.stem != "__init__":
            import_module(f".{file.stem}", __package__)
