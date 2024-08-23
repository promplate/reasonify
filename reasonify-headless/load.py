import sys
from functools import cache
from os import chdir
from pathlib import Path
from typing import TYPE_CHECKING, Awaitable, Callable

from js import FileSystemDirectoryHandle, window
from micropip import install
from pyodide.ffi import create_once_callable, create_proxy
from pyodide.webloop import PyodideFuture

if TYPE_CHECKING:
    sources: dict[str, str] = {}

    def with_toast[**Params, Return](message: str) -> Callable[[Callable[Params, Return]], Callable[Params, PyodideFuture[Return]]]: ...


for path, source in sources.items():
    file = Path("/home/pyodide", path)
    if not file.parent.is_dir():
        file.parent.mkdir(parents=True)
    file.write_text(source, "utf-8")


if __debug__:
    for module in tuple(sys.modules):  # for HMR
        if module.startswith("reasonify"):
            sys.modules.pop(module).__dict__.clear()

if TYPE_CHECKING:

    class NativeFS:
        syncfs: Callable[[], Awaitable[None]]

    def mount(target: str, handle: FileSystemDirectoryHandle) -> Awaitable[NativeFS]: ...

else:
    from pyodide_js import mountNativeFS as mount


@cache
def install_slugify():
    @with_toast("installing slugify")
    @create_once_callable
    async def install_slugify():
        await install("python-slugify")

    return install_slugify()


@create_proxy
async def mount_native_fs():
    handle = await window.showDirectoryPicker()
    while await handle.requestPermission({"mode": "readwrite"}) != "granted":
        pass

    await install_slugify()
    from slugify import slugify

    name = slugify(handle.name)

    fs = await mount(path := str(root / name), handle)

    mounted[path] = fs

    return name


root = Path("/workspace/mnt")

root.mkdir(parents=True, exist_ok=True)

chdir(root)

mounted: dict[str, "NativeFS"] = {}
