import type { PyProxy } from "pyodide/ffi";

import { type PyProxyTo, toJs } from "./common";
import generate from "./generate";
import getGlobals from "./globals";
import { getPy } from "./load";
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

  const [py, { default: source }] = await Promise.all([
    getPy(),
    import("./load.py?raw"),
  ]);
  await py.runPythonAsync(source);

  const loadReasonify = await getGlobals<() => Promise<PyProxy>>("get_reasonify_chain")();

  const chain = await loadReasonify();
  reasonifyReady.set(true);

  stopIconAnimation();

  return asChain(chain);
}
