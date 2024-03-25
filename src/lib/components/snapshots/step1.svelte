<script lang="ts">
  import type { Step1 } from ".";

  export let context: Step1;
</script>

{#if context.response}
  <div class="text-orange-3">
    {context.response}
  </div>
{:else if context.tools}
  <ul class="flex flex-row gap-1">
    {#each context.tools as tool}
      <li class="rounded bg-cyan-3/10 px-1.5 py-1 text-cyan-3">{tool.name}</li>
    {/each}
  </ul>
{/if}
