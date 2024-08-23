import { getApi } from "./api";
import { withToast } from "$lib/utils/toast";

export async function mount(): Promise<string> {
  const mount = getApi<() => Promise<string>>("api.fs.mount_native_fs");
  return withToast("selecting a directory to mount", (name) => (`mounted ${name}`))(mount)();
}

export async function addFiles(): Promise<string[]> {
  const mount = getApi<() => Promise<string[]>>("api.fs.add_single_files");
  return withToast("selecting files to add to workspace", (names: string[]) => (names.length === 1 ? `added ${names[0]}` : `added ${names.length} files`))(mount)();
}
