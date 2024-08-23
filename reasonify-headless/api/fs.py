import sys
from functools import cache
from os import chdir
from pathlib import Path

from bridge import with_toast
from js import window
from pyodide.ffi import JsBuffer, create_once_callable, create_proxy
from utils.fs import NativeFS, mount, unmount
from utils.to_js import to_js


@cache
def _install_slugify():
    @with_toast("installing slugify")
    @create_once_callable
    async def install_slugify():
        from reasonify.tools.install import pip_install

        await pip_install("python-slugify")

    return install_slugify()


mounted: dict[str, NativeFS] = {}
single_files = set[str]()


@create_proxy
async def mount_native_fs():
    install_promise = _install_slugify()

    handle = await window.showDirectoryPicker()
    while await handle.requestPermission(to_js({"mode": "readwrite"})) != "granted":
        pass

    await install_promise

    from slugify import slugify

    name = slugify(handle.name)

    fs = await mount(path := str(root / name), handle)

    mounted[path] = fs

    return name


async def add_single_files():
    handles = await window.showOpenFilePicker(to_js({"multiple": True}))

    names = []

    for handle in handles:
        path = root / handle.name
        buffer: JsBuffer = await (await handle.getFile()).arrayBuffer()
        with path.open("w") as f:
            buffer.to_file(f)
        single_files.add(str(path))
        names.append(handle.name)

    return to_js([handle.name for handle in handles])


async def sync_all():
    for name, fs in mounted.items():
        await with_toast(f"syncing {Path(name).name}")(fs.syncfs)()


def reset():
    for path in single_files:
        Path(path).unlink()
    single_files.clear()

    for path in mounted:
        unmount(path)
        Path(path).rmdir()
    mounted.clear()


root = Path("/workspace/mnt")
root.mkdir(parents=True, exist_ok=True)
chdir(root)
sys.path.append(str(root))
