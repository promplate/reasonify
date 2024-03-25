import type { Tool } from "..";
import type { PyCallable } from "pyodide/ffi";

import code from "./run.py?raw";
import schema from "./schema.ts?raw";
import { getPy } from "$lib/py";
import { cacheSingleton } from "$lib/utils/cache";
import { formatSchemaPrompt } from "$lib/utils/format";

const instruction = `
The "source" field must be a runnable python script.
You can read the stdout/stderr and the values you created as the tool's output.
`.trim();

const getRun = cacheSingleton(async () => {
  const py = await getPy();
  await py.runPythonAsync(code);
  return py.globals.get("run") as PyCallable;
});

export default {
  id: "py",
  name: "Python Interpreter",
  usage: "Run some python code. You can only use the standard library. Open your mind. If something can be done through code, then don't ask the user.",
  schema: formatSchemaPrompt(schema),
  instruction,
  run: async options => await (await getRun()).callKwargs(options),
} as Tool;
