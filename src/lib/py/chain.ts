import type { PyProxy } from "pyodide/ffi";

import sources from "../../../reasonify-headless";
import { type PyProxyTo, toJs } from "./common";
import generate from "./generate";
import { getPy } from "./load";
import requirements from "./requirements";
import { reasonifyReady } from "$lib/stores";
import { startIconAnimation, stopIconAnimation } from "$lib/stores/icon";

export interface Chain {
  astream: <T extends object>(context: T) => AsyncGenerator<T & { result: string }>;
}

type ChainContext<T> = PyProxyTo<T> & { result: string };

function asChain(chain: PyProxy) {
  return {
    async *astream<T>(context: T) {
      const py = await getPy();
      let ctx: ChainContext<T>;
      for await (ctx of chain.astream(py.toPy(context), generate)) {
        yield { ...toJs((ctx)), result: ctx.result };
      }
      yield { ...toJs((ctx!)), result: ctx!.result };
    },
  };
}

export async function initChain() {
  startIconAnimation();

  const py = await getPy();

  py.globals.set("sources", py.toPy(sources));
  await py.pyimport("micropip.install")(requirements);
  await py.runPythonAsync(sources["load.py"]);
  py.pyimport("utils.ask.register_self_as_tool")(generate);

  stopIconAnimation();

  reasonifyReady.set(true);

  return asChain(py.pyimport("reasonify.chain"));
}
