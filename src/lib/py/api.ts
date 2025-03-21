import type { PyCallable, PyProxy } from "pyodide/ffi";

import { py } from "./load";

const cache = new Map<string, PyProxy>();

export function getApi<T = () => any>(slug: string): T {
  if (cache.has(slug)) {
    return cache.get(slug) as T;
  } else {
    const api = py.pyimport(slug) as T & PyCallable;
    cache.set(slug, api);
    return api;
  }
}

export function clearApiCache() {
  cache.forEach(value => value.destroy());
  cache.clear();
}
