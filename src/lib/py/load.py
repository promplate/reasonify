from asyncio import sleep
from contextlib import suppress
from os import getenv
from typing import TYPE_CHECKING, Awaitable, Callable
from zipfile import BadZipFile

from micropip import install
from pyodide.ffi import create_once_callable

if TYPE_CHECKING:

    def with_toast[**Params, Return](message: str) -> Callable[[Callable[Params, Return]], Callable[Params, Awaitable[Return]]]: ...


async def get_reasonify_chain():
    requirement = getenv("PACKAGE", "reasonify-headless")
    if requirement.endswith(".whl"):
        r = requirement[requirement.index("reasonify") : requirement.index("-py3-none")].replace("-", "==").replace("_", "-")
    else:
        r = requirement

    @with_toast(f"installing {r}")
    @create_once_callable
    async def install_reasonify():
        while True:
            with suppress(BadZipFile):
                return await install(requirement)
            await sleep(0.1)

    await install_reasonify()

    from reasonify import chain

    return chain
