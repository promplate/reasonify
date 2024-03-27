from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from traceback import format_exception_only

from promplate import Context
from pyodide.code import eval_code_async


def diff_context(context_in: Context, context_out: Context):
    return {
        k: v for k, v in context_out.items() if not k.startswith("__") and (k not in context_in or context_in[k] != v)
    }


async def run(source: str):
    context = {"__name__": "__main__"}

    original_context = context.copy()

    result = None

    io = StringIO()

    with redirect_stdout(io), redirect_stderr(io):
        try:
            result = await eval_code_async(source, context)
        except Exception as e:
            io.write("\n".join(format_exception_only(e)))

    out = {"global values": diff_context(original_context, context), "stdout/stderr": io.getvalue()}
    if result is not None:
        out["return"] = result

    return out
