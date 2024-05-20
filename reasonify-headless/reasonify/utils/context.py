from functools import partial
from typing import TYPE_CHECKING

from partial_json_parser import ALL
from promplate import ChainContext
from promptools.extractors.json import extract_json


class Context(ChainContext):
    def __init__(self, context: ChainContext):
        if not isinstance(context.get("snapshots"), list):
            context["snapshots"] = []
        super().__init__(context)

    @property
    def snapshots(self) -> list[dict]:
        return self["snapshots"]

    def __setitem__(self, key, value):
        try:
            self.snapshots[0][key] = value
        except IndexError:
            super().__setitem__(key, value)

    def __delitem__(self, key: str):
        try:
            del self.snapshots[0][key]
        except KeyError:
            super().__delitem__(key)

    def __getitem__(self, key: str):
        if key != "snapshots":
            for snapshot in self.snapshots:
                if key in snapshot:
                    return snapshot[key]
        return super().__getitem__(key)

    def __contains__(self, key):
        if key != "snapshots" and key in self.snapshots[0]:
            return True
        return super().__contains__(key)

    if TYPE_CHECKING:

        @property
        def extract_json(self):
            return partial(extract_json, self.result)

    else:

        def extract_json(self, fallback=None, expect=None, allow_partial=ALL):
            try:
                return extract_json(self.result, fallback, expect, allow_partial)
            except NameError:  # pydantic v1
                # NameError: Field name "schema" shadows a BaseModel attribute; use a different field name with "alias='schema'".
                return extract_json(self.result, fallback, allow_partial=allow_partial)


def new_checkpoint(context):
    Context.ensure(context).snapshots.insert(0, {})
