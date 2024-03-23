import { getChain, getPy } from "./load";
import { toast } from "svelte-sonner";

export * from "./load";

export default async () => {
  const text = "Initiating runtime environment ...";
  toast.promise(getChain, { loading: text, success: text });
  return await getPy();
};
