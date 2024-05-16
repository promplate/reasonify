import type { Tool } from "..";
import type { PyCallable } from "pyodide/ffi";

import code from "./run.py?raw";
import schema from "./schema.ts?raw";
import { getPy } from "$lib/py";
import { cacheSingleton } from "$lib/utils/cache";
import { formatSchemaPrompt } from "$lib/utils/format";
import { withToast } from "$lib/utils/toast";

const instruction = `
The "source" field must be a runnable python script.
You can read the stdout/stderr and the values you created as the tool's output.
The runtime environment is an IPython-like console. Top-level await is supported.
You can use "input()" inside code to get user's information, but don't use too much!
`.trim();

const getRun = cacheSingleton(async () => {
  const py = await getPy();
  await py.runPythonAsync(code);
  return py.globals.get("run") as PyCallable;
});

export default {
  id: "py",
  name: "Python Interpreter",
  usage: "Run some python code. Open your mind. If something can be done through code, then don't use other tools.",
  schema: formatSchemaPrompt(schema),
  instruction,
  run: withToast("running python code")(async options => await (await getRun()).callKwargs(options)),
} as Tool;
