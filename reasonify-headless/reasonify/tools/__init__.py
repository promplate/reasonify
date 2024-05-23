from importlib import import_module
from pathlib import Path
from traceback import format_exception_only


def register_all():
    for file in Path(__file__).parent.glob("*.py"):
        if file.stem != "__init__":
            try:
                import_module(f".{file.stem}", __package__)
            except Exception as e:
                print(f"during registering tools inside {file = !s}: \n", format_exception_only(e)[0].strip())
