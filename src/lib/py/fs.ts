import { getApi } from "./api";
import { withToast } from "$lib/utils/toast";

export async function mount(): Promise<string> {
  const mount = getApi<() => Promise<string>>("api.fs.mount_native_fs");
  return withToast("selecting a directory to mount", (name) => (`mounted ${name}`))(mount)();
}
