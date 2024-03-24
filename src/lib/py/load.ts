import type { PyCallable } from "pyodide/ffi";

import chat from "../chat";
import { promplateReady, pyodideReady, reasonifyReady } from "../stores";
import { dev } from "$app/environment";
import { cacheSingleton } from "$lib/utils/cache";

const indexURL = "https://cdn.jsdelivr.net/pyodide/v0.25.0/full/";

export const getPy = cacheSingleton(async () => {
  const { loadPyodide } = await import("pyodide");
  const PACKAGE = dev ? "/whl/reasonify_headless-0.0.1-py3-none-any.whl" : "reasonify-headless==0.0.1";
  const py = await loadPyodide({ indexURL, packages: ["micropip", "typing-extensions"], env: { PACKAGE }, args: ["-O"] });
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
  const loadReasonify: (patcher: CallableFunction) => Promise<Chain> = py.globals.get("get_reasonify_chain");

  const chain = await loadReasonify(() => loadPromplate().then(() => promplateReady.set(true)));
  reasonifyReady.set(true);
  return chain;
});

interface Chain {
  astream: PyCallable;
}

export const getGenerate = cacheSingleton(async () => {
  const py = await getPy();
  return py.globals.get("make_generate")(chat);
});
