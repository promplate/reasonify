import sys
from functools import cache
from os import chdir
from pathlib import Path

from bridge import with_toast
from js import window
from pyodide.ffi import create_once_callable, create_proxy
from utils.fs import NativeFS, mount


@cache
def _install_slugify():
    @with_toast("installing slugify")
    @create_once_callable
    async def install_slugify():
        from reasonify.tools.install import pip_install

        await pip_install("python-slugify")

    return install_slugify()


mounted: dict[str, NativeFS] = {}


@create_proxy
async def mount_native_fs():
    install_promise = _install_slugify()

    handle = await window.showDirectoryPicker()
    while await handle.requestPermission({"mode": "readwrite"}) != "granted":
        pass

    await install_promise

    from slugify import slugify

    name = slugify(handle.name)

    fs = await mount(path := str(root / name), handle)

    mounted[path] = fs

    return name


root = Path("/workspace/mnt")
root.mkdir(parents=True, exist_ok=True)
chdir(root)
sys.path.append(str(root))
