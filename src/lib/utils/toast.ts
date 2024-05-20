import type { PythonError } from "pyodide/ffi";

import { toast } from "svelte-sonner";

function displayError(error: any) {
  if (error instanceof Error && error.name === "PythonError")
    return (error as PythonError).message;
  return String(error);
}

export function withToast<T extends (...args: any[]) => any>(message: string, success?: string | ((data: ReturnType<T>) => string)) {
  return (anyFunction: T) => {
    return (async (...args) => {
      const promise: Promise<ReturnType<T>> = Promise.resolve(anyFunction(...args));
      toast.promise(promise, { loading: message, success: success ?? message, error: displayError });
      const result = await promise;
      return result;
    }) as T;
  };
}
