from asyncio import sleep
from contextlib import suppress
from os import chdir, getenv
from pathlib import Path
from typing import TYPE_CHECKING, Awaitable, Callable
from zipfile import BadZipFile

from js import FileSystemDirectoryHandle, window
from micropip import install
from pyodide.ffi import create_once_callable, create_proxy

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


if TYPE_CHECKING:

    class NativeFS:
        syncfs: Callable[[], Awaitable[None]]

    def mount(target: str, handle: FileSystemDirectoryHandle) -> Awaitable[NativeFS]: ...

else:
    from pyodide_js import mountNativeFS as mount


@create_proxy
async def mount_native_fs():
    handle = await window.showDirectoryPicker()
    while await handle.requestPermission({"mode": "readwrite"}) != "granted":
        pass

    fs = await mount(path := str(root / handle.name), handle)

    mounted[path] = fs

    return handle.name


root = Path("/workspace/mnt")

root.mkdir(parents=True, exist_ok=True)

chdir(root)

mounted: dict[str, "NativeFS"] = {}
