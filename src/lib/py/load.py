from asyncio import gather
from os import getenv

from micropip import install


async def patch_promplate():
    await install(["promplate-pyodide~=0.0.2.2"])

    from promplate_pyodide import patch_promplate

    patch_promplate()


async def get_reasonify_chain(patch_promplate=patch_promplate):
    await gather(patch_promplate(), install(getenv("PACKAGE", "reasonify-headless")))

    from reasonify import chain

    return chain
