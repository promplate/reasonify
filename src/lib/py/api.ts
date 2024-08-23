import { py } from "./load";

const cache = new Map<string, any>();

export function getApi<T>(slug: string): T {
  if (cache.has(slug)) {
    return cache.get(slug) as T;
  } else {
    const api = py.pyimport(slug) as T;
    cache.set(slug, api);
    return api;
  }
}

export function clearApiCache() {
  cache.clear();
}
