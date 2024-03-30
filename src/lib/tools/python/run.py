from contextlib import redirect_stderr, redirect_stdout, suppress
from functools import cache
from io import StringIO
from json import dumps, loads
from traceback import format_exception_only

from promplate import Context
from pyodide.code import eval_code_async

from reasonify.utils.serialize import RobustEncoder


@cache
def get_context():
    return {"__name__": "__main__"}


def is_different(a, b):
    with suppress(ValueError):
        return bool(a != b)

    return a is not b


def diff_context(context_in: Context, context_out: Context):
    return {
        k: v
        for k, v in context_out.items()
        if not k.startswith("__") and (k not in context_in or is_different(context_in[k], v))
    }


async def install_requirements(requirements: list[str]):
    from micropip import install

    await install(requirements, verbose=True, keep_going=True)


async def run(source: str, requirements: list[str] | None = None):
    context = get_context()

    original_context = context.copy()

    result = None

    io = StringIO()

    with redirect_stdout(io), redirect_stderr(io):
        try:
            if requirements:
                await install_requirements(requirements)

            result = await eval_code_async(source, context)
        except Exception as e:
            io.write("\n".join(format_exception_only(e)))

    out = {"global values": diff_context(original_context, context), "stdout/stderr": io.getvalue()}
    if result is not None:
        out["return"] = result

    return loads(dumps(out, cls=RobustEncoder))  # ensure serializable
