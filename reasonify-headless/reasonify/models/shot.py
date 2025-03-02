from typing import Literal

from promplate.prompt.chat import Message, assistant, system, user
from pydantic import BaseModel, Field

from ..utils.run import Result, run
from ..utils.serialize import json


class Run(BaseModel):
    source: str
    result: dict | Literal[False] | None = None

    async def ensure_result(self) -> Result | str:
        match self.result:
            case False:
                return "<omitted>"
            case None:
                return await run(self.source)
            case _:
                mixed = self.result
                result: Result = {}
                if "return" in mixed:
                    result["return"] = mixed.pop("return")
                if "stdout/stderr" in mixed:
                    result["stdout/stderr"] = mixed.pop("stdout/stderr")
                if mixed:
                    result["global values"] = mixed
                return result


class Shot(BaseModel):
    title: str = Field(pattern=r"[a-z_0-9]+")

    interactions: list[list[Run] | str]

    async def get_messages(self) -> list[Message]:
        messages = []

        for i in self.interactions:
            if isinstance(i, str):
                messages.append(user @ f"example_user_{self.title}" > i)
            else:
                sources, results = zip(*[(run.source, await run.ensure_result()) for run in i])

                messages.append(assistant @ f"example_assistant_{self.title}" > json(sources))
                messages.append(system @ f"example_results_{self.title}" > json(results))

        return messages
