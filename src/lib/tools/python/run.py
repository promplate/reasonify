from promplate import Context
from pyodide.console import Console


def diff_context(context_in: Context, context_out: Context):
    return {
        k: v for k, v in context_out.items() if not k.startswith("__") and (k not in context_in or context_in[k] != v)
    }


async def run(source: str):
    context = {"__name__": "__main__"}

    output = []

    console = Console(context, stdout_callback=output.append, stderr_callback=output.append)

    original_context = context.copy()

    result = None

    for line in source.splitlines():
        try:
            future = console.push(line)
            result = await future
        except Exception:
            output.append(future.formatted_error)
            break

    out = {"values": diff_context(original_context, context), "stdout/stderr": "".join(output)}
    if result is not None:
        out["result"] = result

    return out
