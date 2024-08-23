import sys
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    sources: dict[str, str] = {}


for path, source in sources.items():
    file = Path("/home/pyodide", path)
    if not file.parent.is_dir():
        file.parent.mkdir(parents=True)
    file.write_text(source, "utf-8")


if __debug__:
    for module in tuple(sys.modules):  # for HMR
        if module.startswith("reasonify") or module.startswith("promplate_recipes"):
            del sys.modules[module]
