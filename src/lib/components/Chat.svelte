<script lang="ts">
  import type { AgentWrapper } from "../py";
  import type { Context } from "../types";
  import type { PythonError } from "pyodide/ffi";

  import { initChain } from "../py";
  import { clearApiCache, getApi } from "../py/api";
  import Highlight from "./Highlight.svelte";
  import Markdown from "./Markdown.svelte";
  import { dev } from "$app/environment";
  import { addFiles, mount } from "$lib/py/fs";
  import { pyodideReady, reasonifyReady, startIconAnimation, stopIconAnimation } from "$lib/stores";
  import { toast } from "svelte-sonner";

  export let chain: AgentWrapper;

  let content = "";
  let running = false;
  let refreshing = false;
  let context: Context | undefined;

  $: messages = context?.messages ?? [];

  async function refresh() {
    refreshing = true;
    try {
      $reasonifyReady = false;
      clearApiCache();
      chain = await initChain();
    } finally {
      refreshing = false;
    }
  }

  async function start() {
    running = true;
    try {
      for await (const i of chain.astream({ query: content })) context = i;
    } catch (e) {
      toast.error((e as PythonError).message);
    } finally {
      running = false;
    }
  }

  $: running ? startIconAnimation() : stopIconAnimation();

</script>

<main class="mb-35 w-screen flex flex-col justify-between -mt-1px md:(mb-50 mt-10 w-[min(70rem,calc(100vw-5rem))])">
  <div class="group w-full flex flex-col-reverse text-sm">
    {#each context?.snapshots ?? [] as ctx, i}
      <div class="relative flex flex-col gap-4.5 overflow-scroll border-t-1 border-neutral-6 border-dashed p-5 hover:(border-neutral-4 border-solid bg-white/2) md:p-7">
        <div>
          <span class="bg-neutral-2 text-neutral-9">
            {messages.filter(msg => msg.role === "user").at(-1 - i)?.content}
          </span>
        </div>
        {#if ctx.response?.length}
          <section class="flex flex-col gap-1">
            {#each ctx.response ?? [] as text}
              <Markdown {text} langs={["python"]} />
            {/each}
          </section>
        {/if}
        {#if ctx.sources?.length}
          {#each ctx.sources as source, j}
            {#if i === 0}
              <!-- the last snapshot -->
              <div class="transition-opacity" class:op-50={running && j + 1 !== ctx.sources.length && ctx.sources.length !== ctx.results?.length}>
                <div class="animate-(fade-in duration-300)">
                  <Highlight {source} lang="python" />
                </div>
              </div>
            {:else}
              <!-- non-last snapshots -->
              <Highlight {source} lang="python" />
            {/if}
          {/each}
        {/if}
        {#if ctx.results?.length}
          {@const entries = ctx.results.flatMap(Object.entries)}
          {#if entries.length}
            <Highlight source={JSON.stringify(Object.fromEntries(entries), null, 4)} lang="json" />
          {/if}
        {/if}
        <div class="absolute right-0 top-0 flex flex-row translate-x-0.25em select-none items-center text-7xl op-5 -translate-y-2/7">
          <span class="font-bold font-fira">&lt;/</span>
          <span class="font-fancy">{ctx.results?.length ?? 0}</span>
          <span class="font-bold font-fira">/&gt;</span>
        </div>
      </div>
    {/each}
  </div>
</main>

<div class="fixed bottom-0 left-0 w-full bg-neutral-8/90 md:(bottom-10 left-1/2 w-[min(70rem,calc(100vw-5rem))] rounded -translate-x-1/2)">
  <textarea class="h-35 w-full resize-none bg-transparent p-5 outline-none md:h-40 md:p-7 <md:text-sm placeholder-neutral-5" placeholder="type your query here" bind:value={content} />
  <div class="absolute bottom-4 right-4 flex flex-row gap-2 md:(bottom-6 right-6 gap-3) [&>button]:(grid place-items-center rounded bg-white p-2 text-neutral-9 transition md:p-3 md:text-lg) [&>button:disabled]:(bg-white/10 text-white)">
    <button disabled={!content || running} on:click={start}>
      <div class="i-lucide-plane-takeoff" />
    </button>
    <button disabled={!$pyodideReady} on:click={async () => {
      const names = await addFiles();
      chain.pushMessage({ role: "system", name: "info", content: `user added ${names.length} files: ${(names.map(name => `./${name}`)).join(", ")}` });
    }}>
      <div class="i-lucide-file-symlink" />
    </button>
    {#if "showDirectoryPicker" in window}
      <button disabled={!$pyodideReady} on:click={async () => {
        const name = await mount();
        chain.pushMessage({ role: "system", name: "info", content: `user mounted a directory: ./${name}` });
      }}>
        <div class="i-lucide-folder-symlink" />
      </button>
      <button disabled={!$pyodideReady} on:click={async () => {
        const syncAll = getApi("api.fs.sync_all");
        await syncAll();
      }}>
        <div class="i-lucide-hard-drive-download" />
      </button>
    {/if}
    {#if dev}
      <button disabled={refreshing} on:click={refresh}>
        <div class="i-lucide-refresh-cw" />
      </button>
    {/if}
    <button disabled={!messages.length || running} on:click={() => {
      context = undefined;
      getApi("api.fs.reset")();
      chain.reset();
    }}>
      <div class="i-lucide-circle-fading-plus" />
    </button>
  </div>
</div>
