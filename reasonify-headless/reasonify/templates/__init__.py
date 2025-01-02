from pathlib import Path

from promplate_recipes import DotTemplate
from promplate_recipes.context import register_components

root = Path(__file__).parent

register_components(root)

main = DotTemplate.read(root / "main.j2")
