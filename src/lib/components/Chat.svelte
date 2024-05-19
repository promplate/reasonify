<script lang="ts">
  import type { Context, Message } from "../types";
  import type { PythonError } from "pyodide/ffi";

  import { type Chain, getPy, initChain } from "../py";
  import { dev } from "$app/environment";
  import { pyodideReady, reasonifyReady, startIconAnimation, stopIconAnimation } from "$lib/stores";
  import { globalCache } from "$lib/utils/cache";
  import { toast } from "svelte-sonner";

  export let chain: Chain;

  let content = "";
  let running = false;
  let refreshing = false;
  let context: Context;

  async function refresh() {
    refreshing = true;
    try {
      getPy.invalidateCache();
      globalCache.clear();
      $pyodideReady = false;
      $reasonifyReady = false;
      chain = await initChain();
    } finally {
      refreshing = false;
    }
  }

  async function start() {
    const messages: Message[] = [{ role: "user", content }];
    context = { messages };
    running = true;
    try {
      for await (const i of chain.astream(context)) context = i;
    } catch (e) {
      toast.error((e as PythonError).message);
    } finally {
      running = false;
    }
  }

  $: running ? startIconAnimation() : stopIconAnimation();

</script>

<main class="mb-50 mt-10 w-[min(70rem,calc(100vw-5rem))] flex flex-col justify-between">
  <div class="group w-full flex flex-col-reverse text-sm">
    {#each context?.snapshots ?? [] as ctx, i}
      <div class="relative overflow-scroll border-t-1 border-neutral-6 border-dashed px-7 py-7 hover:(border-neutral-4 border-solid bg-white/2)">
        <pre>{JSON.stringify(ctx, null, 2)}</pre>
        <div class="absolute right-0 top-0 flex flex-row translate-x-0.25em select-none items-center text-7xl op-5 -translate-y-2/7">
          <span class="font-bold font-mono">&lt;/</span>
          <span class="font-fancy">{i}</span>
          <span class="font-bold font-mono">/&gt;</span>
        </div>
      </div>
    {/each}
  </div>
</main>

<div class="fixed bottom-10 left-1/2 w-[min(70rem,calc(100vw-5rem))] rounded bg-neutral-8/90 -translate-x-1/2">
  <textarea class="h-40 w-full resize-none bg-transparent p-7 outline-none placeholder-neutral-5" placeholder="type your query here" bind:value={content} />
  <div class="absolute bottom-6 right-6 flex flex-row gap-3 [&>button]:(grid place-items-center rounded bg-white p-3 text-lg text-neutral-9 transition) [&>button:disabled]:(bg-white/10 text-white)">
    <button disabled={!content || running} on:click={start}>
      <div class="i-lucide-plane-takeoff" />
    </button>
    {#if dev}
      <button disabled={refreshing} on:click={refresh}>
        <div class="i-lucide-refresh-cw" />
      </button>
    {/if}
  </div>
</div>
