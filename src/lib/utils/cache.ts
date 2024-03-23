export function cacheSingleton<R, F extends () => R>(target: F) {
  const UNSET = {};
  let result: R | object = UNSET;

  return (() => {
    if (result !== UNSET)
      return result as R;

    result = target();
    return result;
  }) as F;
}
