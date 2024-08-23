from typing import TYPE_CHECKING, Awaitable, Callable

from js import FileSystemDirectoryHandle

if TYPE_CHECKING:

    class NativeFS:
        syncfs: Callable[[], Awaitable[None]]

    def mount(target: str, handle: FileSystemDirectoryHandle) -> Awaitable[NativeFS]: ...
    def unmount(target: str) -> None: ...

else:
    from pyodide_js import mountNativeFS as mount
    from pyodide_js.FS import unmount

    NativeFS = object

__all__ = ["mount", "unmount", "NativeFS"]
