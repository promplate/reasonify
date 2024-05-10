import type { PyProxy } from "pyodide/ffi";

import chat from "../chat";
import { promplateReady, pyodideReady, reasonifyReady } from "../stores";
import VERSION from "./version";
import { dev } from "$app/environment";
import * as env from "$env/static/public";
import { cacheSingleton } from "$lib/utils/cache";
import { version } from "pyodide";

const indexURL = ("PUBLIC_PYODIDE_INDEX_URL" in env) ? (env.PUBLIC_PYODIDE_INDEX_URL as string).replace("{}", version) : `https://cdn.jsdelivr.net/pyodide/v${version}/full/`;

export const getPy = cacheSingleton(async () => {
  const { loadPyodide } = await import("pyodide");
  const PACKAGE = dev ? `/whl/reasonify_headless-${VERSION}-py3-none-any.whl` : `reasonify-headless==${VERSION}`;
  const py = await loadPyodide({ indexURL, packages: ["micropip", "typing-extensions"], env: { PACKAGE }, args: ["-OO"] });
  pyodideReady.set(true);
  return py;
});

export const getChain = cacheSingleton(async () => {
  const [py, { default: source }] = await Promise.all([
    getPy(),
    import("./load.py?raw"),
  ]);
  await py.runPythonAsync(source);

  const loadPromplate: () => Promise<void> = py.globals.get("patch_promplate");
  const loadReasonify: (patcher: CallableFunction) => Promise<PyProxy> = py.globals.get("get_reasonify_chain");

  const chain = await loadReasonify(() => loadPromplate().then(() => promplateReady.set(true)));
  reasonifyReady.set(true);

  return {
    async *astream(context) {
      const dict = await getDict();
      for await (const proxy of chain.astream(context, await getGenerate())) {
        const { result } = proxy;
        yield { ...dict(proxy).toJs({ dict_converter: Object.fromEntries }), result };
      }
    },
  } as Chain;
});

export interface Chain {
  astream: <T extends object>(context: T) => AsyncGenerator<T & { result: string }>;
}

interface PyProxyTo<T> extends PyProxy {
  toJs: (...args: Parameters<PyProxy["toJs"]>) => T;
}

const getGenerate = cacheSingleton(async () => {
  const py = await getPy();
  return py.globals.get("make_generate")(chat);
});

const getDict = cacheSingleton(async () => {
  const py = await getPy();
  return py.globals.get("dict") as (obj: PyProxy) => PyProxyTo<object>;
});
