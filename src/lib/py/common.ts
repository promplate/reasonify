import type { PyProxy } from "pyodide/ffi";

import { isObj } from "openai/core.mjs";

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
