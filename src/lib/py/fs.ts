import getGlobals from "./globals";
import { withToast } from "$lib/utils/toast";

const getMount = getGlobals<() => Promise<string>>("mount_native_fs");

export async function mount(): Promise<string> {
  const mount = await getMount();
  return withToast("selecting a directory to mount", (name) => (`mounted ${name}`))(mount)();
}
