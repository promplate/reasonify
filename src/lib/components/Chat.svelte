<script lang="ts">
  import type { Context } from "../types";
  import type { PythonError } from "pyodide/ffi";

  import { type Chain, getPy, initChain } from "../py";
  import Highlight from "./Highlight.svelte";
  import Markdown from "./Markdown.svelte";
  import { dev } from "$app/environment";
  import { mount } from "$lib/py/fs";
  import { pyodideReady, reasonifyReady, startIconAnimation, stopIconAnimation } from "$lib/stores";
  import { globalCache } from "$lib/utils/cache";
  import { toast } from "svelte-sonner";

  export let chain: Chain;

  let content = "";
  let running = false;
  let refreshing = false;
  let context: Context = { query: content };

  $: messages = context?.messages ?? [];

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
    context = { ...context, query: content };
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
    {#each context?.snapshots ?? [] as ctx}
      <div class="relative flex flex-col gap-4.5 overflow-scroll border-t-1 border-neutral-6 border-dashed px-7 py-7 hover:(border-neutral-4 border-solid bg-white/2)">
        {#if ctx.response?.length}
          <section class="flex flex-col gap-1">
            {#each ctx.response ?? [] as text}
              <Markdown {text} langs={["python"]} />
            {/each}
          </section>
        {/if}
        {#if ctx.sources?.length}
          <Highlight source={ctx.sources.join("\n")} lang="python" />
        {/if}
        {#if ctx.results?.length}
          <Highlight source={JSON.stringify(Object.assign({}, ...ctx.results), null, 4)} lang="json" />
        {/if}
        <div class="absolute right-0 top-0 flex flex-row translate-x-0.25em select-none items-center text-7xl op-5 -translate-y-2/7">
          <span class="font-bold font-fira">&lt;/</span>
          <span class="font-fancy">{ctx.index ?? 0}</span>
          <span class="font-bold font-fira">/&gt;</span>
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
    <button disabled={!$pyodideReady} on:click={async () => {
      const name = await mount();
      context.messages = [...messages, { role: "system", name: "info", content: `user mounted a directory: ./${name}` }];
    }}>
      <div class="i-lucide-file-symlink" />
    </button>
    {#if dev}
      <button disabled={refreshing} on:click={refresh}>
        <div class="i-lucide-refresh-cw" />
      </button>
    {/if}
    <button disabled={!messages.length || running} on:click={() => {
      context = { query: content };
    }}>
      <div class="i-lucide-circle-fading-plus" />
    </button>
  </div>
</div>
