from typing import TYPE_CHECKING

if TYPE_CHECKING:

    def to_js[T](x: T) -> T: ...

else:
    from pyodide.ffi import to_js

__all__ = ["to_js"]
