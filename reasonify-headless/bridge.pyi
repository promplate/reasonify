from typing import Callable

from pyodide.webloop import PyodideFuture

def with_toast[**Params, Return](message: str) -> Callable[[Callable[Params, Return]], Callable[Params, PyodideFuture[Return]]]: ...
