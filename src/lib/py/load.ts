import { pyodideReady } from "../stores";
import VERSION from "./version";
import { dev } from "$app/environment";
import * as env from "$env/static/public";
import { cacheSingleton } from "$lib/utils/cache";
import { withToast } from "$lib/utils/toast";
import { version } from "pyodide";

const indexURL = ("PUBLIC_PYODIDE_INDEX_URL" in env) ? (env.PUBLIC_PYODIDE_INDEX_URL as string).replace("{}", version) : `https://cdn.jsdelivr.net/pyodide/v${version}/full/`;

export const getPy = cacheSingleton(async () => {
  const { loadPyodide } = await import("pyodide");
  const PACKAGE = dev ? `/whl/reasonify_headless-${VERSION}-py3-none-any.whl` : `reasonify-headless==${VERSION}`;
  const py = await loadPyodide({ indexURL, packages: ["micropip", "typing-extensions"], env: { PACKAGE }, args: dev ? [] : ["-OO"] });
  pyodideReady.set(true);
  py.globals.set("with_toast", withToast);
  return py;
});
