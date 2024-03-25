<script lang="ts">
  import type { Chain } from "../py";
  import type { Context, Message } from "../types";

  import Step1 from "./snapshots/step1.svelte";
  import Step2 from "./snapshots/step2.svelte";
  import Step3 from "./snapshots/step3.svelte";
  import Step4 from "./snapshots/step4.svelte";

  export let chain: Chain;

  let content = "";
  let running = false;
  let context: Context;

  async function start() {
    const { default: all_tools } = await import("$lib/tools");
    const messages: Message[] = [{ role: "user", content }];
    context = { messages, all_tools };
    running = true;
    try {
      for await (const i of chain.astream(context)) context = i;
    }
    finally {
      running = false;
    }
  }
</script>

<main class="mb-50 mt-10 w-[min(70rem,calc(100vw-5rem))] flex flex-col justify-between">
  <div class="max-w-full flex flex-col-reverse text-sm">
    {#each context?.snapshots ?? [] as ctx}
      <div class="w-full overflow-scroll border-t-1 border-neutral-6 border-dashed py-7">
        {#if ctx.step === "step1"}
          <Step1 context={ctx} />
        {:else if ctx.step === "step2"}
          <Step2 context={ctx} />
        {:else if ctx.step === "step3"}
          <Step3 context={ctx} />
        {:else if ctx.step === "step4"}
          <Step4 context={ctx} />
        {:else}
          <pre>{JSON.stringify(ctx, null, 2)}</pre>
        {/if}
      </div>
    {/each}
  </div>
</main>

<div class="fixed bottom-10 left-1/2 w-[min(70rem,calc(100vw-5rem))] rounded bg-neutral-8/90 -translate-x-1/2">
  <textarea class="h-40 w-full resize-none bg-transparent p-7 outline-none placeholder-neutral-5" placeholder="type your query here" bind:value={content} />
  <button class="absolute bottom-6 right-6 grid place-items-center rounded bg-white p-3 text-lg transition disabled:bg-white/10 not-disabled:text-neutral-8" disabled={!content || running} on:click={start}>
    <div class="i-lucide-plane-takeoff" />
  </button>
</div>
