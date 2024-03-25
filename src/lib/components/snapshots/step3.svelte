<script lang="ts">
  import type { Step3 } from ".";

  export let context: Step3;
</script>

<div class="flex flex-col items-start gap-2.5">
  {#if context.note}
    {context.note}
  {/if}

  {#if context.actions}
    <ul class="w-full flex flex-col gap-2.5">
      {#each context.actions as action}
        <li class="w-full flex flex-col items-start gap-2.5">
          <div class="flex flex-row items-center gap-1 text-teal-2">
            <div class="rounded bg-teal-2/10 px-1.5 py-1">{action.tool?.name ?? action.tool_id}</div>
            {#if action.purpose}
              {action.purpose}
            {/if}
          </div>
          {#if action.payload}
            <div class="w-full overflow-scroll rounded bg-white/3 px-3.5 py-3">
              <pre>{JSON.stringify({ input: action.payload, output: action.result }, null, 2)}</pre>
            </div>
          {/if}
        </li>
      {/each}
    </ul>
  {/if}
</div>
