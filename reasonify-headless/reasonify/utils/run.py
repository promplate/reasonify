from contextlib import redirect_stderr, redirect_stdout
from functools import cache
from io import StringIO
from itertools import count
from json import loads
from traceback import format_exception, format_exception_only, walk_tb
from typing import Callable

from promplate import Context

from .serialize import json

try:
    from pyodide.code import eval_code_async
except ModuleNotFoundError:
    from coderunner import eval_code_async


@cache
def get_context() -> Context:
    return {"__name__": "__main__"}


def is_different(a, b):
    if type(a) is type(b) and type(a) in (dict, list, tuple, set, frozenset):
        return a != b
    return a is not b


def diff_context(context_in: Context, context_out: Context):
    return {k: v for k, v in context_out.items() if not k.startswith("__") and (k not in context_in or is_different(context_in[k], v))}


counter = count(1).__next__


async def run(source: str):
    filename = f"In[{counter()}]"

    context = get_context()

    original_context = context.copy()

    io = StringIO()

    result = None

    out = {}

    with redirect_stdout(io), redirect_stderr(io):
        try:
            result = await eval_code_async(source, context, filename=filename)
        except Exception as e:
            io.write(get_clean_traceback(e, filename))

    if diff := diff_context(original_context, context):
        out["global values"] = diff

    if logs := io.getvalue():
        out["stdout/stderr"] = logs

    if result is not None:
        try:
            if result not in diff.values():
                out["return"] = result
        except ValueError as e:
            print(format_exception_only(e))
            if all(is_different(result, v) for v in diff.values()):
                out["return"] = str(result)

    return loads(json(out))  # ensure serializable


def register[T: Callable](function: T) -> T:
    get_context()[function.__name__] = function
    return function


def get_clean_traceback(e: BaseException, filename: str):
    keep_frames = False
    n = 0
    for frame, _ in walk_tb(e.__traceback__):
        if keep_frames:
            n += 1
        elif frame.f_code.co_filename == filename:
            keep_frames = True
            n += 1
    return "".join(format_exception(type(e), e, e.__traceback__, -n))
