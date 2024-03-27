from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from traceback import format_exception_only

from promplate import Context
from pyodide.code import eval_code_async


def diff_context(context_in: Context, context_out: Context):
    return {
        k: v for k, v in context_out.items() if not k.startswith("__") and (k not in context_in or context_in[k] != v)
    }


async def install_requirements(requirements: list[str]):
    from micropip import install

    await install(requirements, verbose=True, keep_going=True)


async def run(source: str, requirements: list[str] | None = None):
    context = {"__name__": "__main__"}

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

    return out
