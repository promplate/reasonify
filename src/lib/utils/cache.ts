export function cacheSingleton<R, F extends () => R>(target: F) {
  const UNSET = {};
  let result: R | object = UNSET;

  const f = (() => {
    if (result !== UNSET)
      return result as R;

    result = target();
    return result;
  }) as F & { invalidateCache: () => void };

  f.invalidateCache = () => {
    result = UNSET;
  };

  return f;
}

const globalCache = new Map<string, unknown>();

export function cached(key: string) {
  return function (func: CallableFunction) {
    return function () {
      if (globalCache.has(key))
        return globalCache.get(key);

      const res = func();
      globalCache.set(key, res);
      return res;
    };
  } as <F extends CallableFunction>(func: F) => F;
}
