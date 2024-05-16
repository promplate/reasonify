import { getPy } from "./load";
import { cached } from "$lib/utils/cache";

export default function<T>(name: string, script?: string) {
  return cached(name)(async () => {
    const py = await getPy();
    if (script)
      py.runPython(script);
    return py.globals.get(name) as T;
  });
}
