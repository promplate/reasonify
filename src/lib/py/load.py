from asyncio import gather
from os import getenv
from typing import TYPE_CHECKING

from micropip import install


async def patch_promplate():
    await install(["promplate-pyodide~=0.0.3"])

    from promplate_pyodide import patch_promplate

    patch_promplate()


async def get_reasonify_chain(patch_promplate=patch_promplate):
    await gather(patch_promplate(), install(getenv("PACKAGE", "reasonify-headless")))

    from reasonify import chain

    return chain


if TYPE_CHECKING:
    from promplate.llm.base import AsyncGenerate


def make_generate(js_generate) -> "AsyncGenerate":
    from promplate.prompt.chat import ensure
    from promplate_pyodide.utils.proxy import to_js

    async def _(prompt, **kwargs):
        async for i in js_generate(to_js((kwargs | {"messages": ensure(prompt), "stream": True}))):
            yield i

    return _
