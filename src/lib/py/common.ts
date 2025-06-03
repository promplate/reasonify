import type { PyProxy } from "pyodide/ffi";

export interface PyProxyTo<T> extends PyProxy {
  toJs: (...args: Parameters<PyProxy["toJs"]>) => T;
}

export function toJs<T>(proxy: PyProxyTo<T>) {
  if (isObj(proxy)) {
    if ("toJs" in proxy)
      return proxy.toJs();

    for (const key in proxy as any)
      (proxy as any)[key] = toJs(proxy[key]);
  }

  return proxy as T;
}

function isObj(obj: unknown): obj is Record<string, unknown> {
  return obj != null && typeof obj === "object" && !Array.isArray(obj);
}
