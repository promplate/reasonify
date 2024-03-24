from pyodide.console import Console


def diff_context(context_in: dict, context_out: dict):
    return {k: v for k, v in context_out.items() if k not in context_in or context_in[k] != v}


async def run(source: str):
    context = {"__name__": "__main__"}

    output = []

    console = Console(context, stdout_callback=output.append, stderr_callback=output.append)

    original_context = context.copy()

    try:
        return {
            "result": await console.push(source),
            "values": diff_context(original_context, context),
            "stdout/stderr": "".join(output),
        }

    except Exception as err:
        output.append(console.formattraceback(err))
        return {
            "values": diff_context(original_context, context),
            "stdout/stderr": "".join(output),
        }
