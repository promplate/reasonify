import type { PyProxy } from "pyodide/ffi";

import { toJs } from "./common";
import generate from "./generate";
import getGlobals from "./globals";
import { getPy } from "./load";
import { reasonifyReady } from "$lib/stores";
import { startIconAnimation, stopIconAnimation } from "$lib/stores/icon";

export interface Chain {
  astream: <T extends object>(context: T) => AsyncGenerator<T & { result: string }>;
}

function asChain(chain: PyProxy): Chain {
  return {
    async *astream(context) {
      const py = await getPy();
      for await (const proxy of chain.astream(py.toPy(context), generate)) {
        const { result } = proxy;
        yield { ...toJs((proxy)), result };
      }
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
