import type { Context, Message } from "$lib/types";
import type { PyProxy } from "pyodide/ffi";

import sources from "../../../reasonify-headless";
import { toJs } from "./common";
import generate from "./generate";
import { getPy } from "./load";
import requirements from "./requirements";
import { reasonifyReady } from "$lib/stores";
import { startIconAnimation, stopIconAnimation } from "$lib/stores/icon";

export class AgentWrapper {
  readonly #proxy: PyProxy;

  constructor(agent: PyProxy) {
    this.#proxy = agent;
  }

  async * astream(context: { query: string }): AsyncGenerator<Context> {
    const py = await getPy();
    for await (const ctx of this.#proxy.astream(py.toPy(context), generate)) {
      yield toJs(ctx);
    }
  }

  async pushMessage(message: Message) {
    const py = await getPy();
    this.#proxy.append_message(py.toPy(message));
  }

  reset() {
    this.#proxy.__init__();
  }
}

export async function initChain() {
  startIconAnimation();

  const py = await getPy();

  py.globals.set("sources", py.toPy(sources));
  await py.pyimport("micropip.install")(requirements);
  await py.runPythonAsync(sources["load.py"]);

  stopIconAnimation();

  reasonifyReady.set(true);

  const pyAgent = py.pyimport("reasonify.Agent")();
  return new AgentWrapper(pyAgent);
}
