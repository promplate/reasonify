import type { PyProxy } from "pyodide/ffi";

import { toJs } from "./common";
import generate from "./generate";
import getGlobals from "./globals";
import { getPy } from "./load";
import { reasonifyReady } from "$lib/stores";

export interface Chain {
  astream: <T extends object>(context: T) => AsyncGenerator<T & { result: string }>;
}

const getDict = getGlobals<(obj: PyProxy) => PyProxy>("dict");

function asChain(chain: PyProxy): Chain {
  return {
    async *astream(context) {
      const py = await getPy();
      const dict = await getDict();
      for await (const proxy of chain.astream(py.toPy(context), generate)) {
        const { result } = proxy;
        yield { ...toJs((dict(proxy))), result };
      }
    },
  };
}

export async function initChain() {
  const [py, { default: source }] = await Promise.all([
    getPy(),
    import("./load.py?raw"),
  ]);
  await py.runPythonAsync(source);

  const loadReasonify = await getGlobals<() => Promise<PyProxy>>("get_reasonify_chain")();

  const chain = await loadReasonify();
  reasonifyReady.set(true);

  return asChain(chain);
}
