from collections import defaultdict
from functools import partial
from json import dumps

from box import Box
from promplate import Context, Template
from promplate.prompt.template import SafeChainMapContext as ChainMap
from promplate.prompt.utils import get_builtins

from .resolve import root
from .serialize import RobustEncoder


class SilentBox(Box):
    def __str__(self):
        return super().__str__() if len(self) else ""


SilentBox = partial(SilentBox, default_box=True)  # type: ignore


class BuiltinsLayer(dict):
    def __getitem__(self, key):
        return get_builtins()[key]

    def __contains__(self, key):
        return key in get_builtins()


components = {i.stem: Template.read(i) for i in root.glob("**/*")}

utilities = {
    "json": lambda obj: dumps(obj, indent=4, ensure_ascii=False, cls=RobustEncoder),
    "join": lambda parts: (parts[0] if len(parts) < 2 else ", ".join(parts[:-1]) + f" and {parts[-1]}"),
}

static_layers = (components | utilities, BuiltinsLayer())


def make_context(context: Context | None = None):
    if context is None:
        return ChainMap(*static_layers, defaultdict(SilentBox))
    return ChainMap(dict(SilentBox(context)), *static_layers, defaultdict(SilentBox))


class DotTemplate(Template):
    def render(self, context=None):
        return super().render(make_context(context))

    async def arender(self, context=None):
        return await super().arender(make_context(context))
