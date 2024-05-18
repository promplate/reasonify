from json import dumps
from pathlib import Path

from promplate_recipes import DotTemplate
from promplate_recipes.context import layers, register_components

from ..utils.serialize import RobustEncoder

root = Path(__file__).parent

register_components(root)

utilities = {
    "json": lambda obj: dumps(obj, indent=4, ensure_ascii=False, cls=RobustEncoder),
    "join": lambda parts: (parts[0] if len(parts) < 2 else ", ".join(parts[:-1]) + f" and {parts[-1]}"),
}

layers.append(utilities)

main = DotTemplate.read(root / "main.j2")
