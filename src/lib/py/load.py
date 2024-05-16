from asyncio import gather, sleep
from functools import wraps
from importlib import reload
from os import getenv
from time import perf_counter
from typing import TYPE_CHECKING, Callable
from zipfile import BadZipFile

from micropip import uninstall
from pyodide.ffi import create_once_callable

if TYPE_CHECKING:
    from micropip import install

    create_proxy = create_once_callable

    def with_toast[T: Callable](message: str) -> Callable[[T], T]: ...

else:
    from micropip import install as _install
    from pyodide.ffi import create_proxy

    @wraps(_install)
    async def install(*args, **kwargs):
        t = perf_counter()
        while True:
            try:
                return await _install(*args, **kwargs)
            except BadZipFile as err:
                if perf_counter() - t > 10:
                    raise err from None
                await sleep(1)


async def patch_promplate():
    await install(["promplate-pyodide~=0.0.3"])

    from promplate_pyodide import patch_promplate

    patch_promplate()


@with_toast("re-installing reasonify")
@create_proxy
async def reload_reasonify_chain():
    uninstall("reasonify-headless")
    await install(getenv("PACKAGE", "reasonify-headless"))

    import reasonify

    if not TYPE_CHECKING:
        reasonify = reload(reasonify)

    return reasonify.chain


@with_toast("installing reasonify")
@create_proxy
async def get_reasonify_chain(patch_promplate=patch_promplate):
    await gather(patch_promplate(), install(getenv("PACKAGE", "reasonify-headless")))

    from js import window
    from promplate.prompt.utils import get_builtins

    from reasonify import chain

    def input(any):
        if (result := window.prompt(str(any))) is None:
            raise EOFError("User refused to input anything.")
        return result

    get_builtins()["input"] = input

    return chain
