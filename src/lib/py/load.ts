import { pyodideReady } from "../stores";
import { dev } from "$app/environment";
import * as env from "$env/static/public";
import { cacheSingleton } from "$lib/utils/cache";
import { withToast } from "$lib/utils/toast";
import { type PyodideInterface, version } from "pyodide";

const indexURL = ("PUBLIC_PYODIDE_INDEX_URL" in env) ? (env.PUBLIC_PYODIDE_INDEX_URL as string).replace("{}", version) : `https://cdn.jsdelivr.net/pyodide/v${version}/full/`;

export const getPy = cacheSingleton(async () => {
  const { loadPyodide } = await import("pyodide");
  const pyodide = await loadPyodide({ indexURL, packages: ["micropip", "typing-extensions"], args: dev ? [] : ["-O"] });
  pyodide.registerJsModule("bridge", { with_toast: withToast });
  pyodideReady.set(true);
  py = pyodide;
  return pyodide;
});

// eslint-disable-next-line import/no-mutable-exports
export let py: PyodideInterface;
