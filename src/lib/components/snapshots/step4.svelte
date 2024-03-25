<script lang="ts">
  import type { Step4 } from ".";

  export let context: Step4;
</script>

<div class="flex flex-col items-start gap-2.5">
  {#if context.summary}
    <div>{context.summary}</div>
  {/if}

  {#if context.message}
    <div class="text-orange-3">{context.message}</div>
  {/if}

  {#if context.action}
    <div class="rounded bg-pink-3/10 px-1.5 py-1 text-pink-3">{context.action}</div>
  {/if}

  {#if context.next_step}
    {#if context.next_step.plan}
      <div class="text-yellow-2">{context.next_step.plan}</div>
    {/if}
    {#each context.next_step.tools ?? [] as tool_id}
      <div class="rounded bg-cyan-3/10 px-1.5 py-1 text-cyan-3">{tool_id}</div>
    {/each}
  {/if}
</div>
