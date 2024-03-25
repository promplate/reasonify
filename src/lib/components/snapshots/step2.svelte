<script lang="ts">
  import type { Step2 } from ".";

  export let context: Step2;
</script>

<div class="flex flex-col items-start gap-2.5">
  {#if context.plan}
    {context.plan}
  {/if}

  {#if context.tools}
    <ul class="flex flex-row gap-1">
      {#each context.tools as tool}
        <li class="rounded bg-cyan-3/10 px-1.5 py-1 text-cyan-3">{tool.name}</li>
      {/each}
    </ul>
  {/if}
</div>
