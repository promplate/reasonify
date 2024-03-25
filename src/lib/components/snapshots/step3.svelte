<script lang="ts">
  import type { Step3 } from ".";

  import Highlight from "../Highlight.svelte";

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
            {#if action.tool_id}
              <div class="rounded bg-teal-2/10 px-1.5 py-1">{action.tool?.name ?? action.tool_id}</div>
            {/if}
            {#if action.purpose}
              {action.purpose}
            {/if}
          </div>
          {#if action.payload}
            <div class="w-full rounded bg-gradient-(from-white/7 via-white/2 to-white/4 to-rb) p-3">
              <div class="w-full overflow-scroll rounded bg-neutral-9 px-3.5 py-3">
                <Highlight lang="json" source={JSON.stringify({ input: action.payload, output: action.result }, null, 2)} />
              </div>
            </div>
          {/if}
        </li>
      {/each}
    </ul>
  {/if}
</div>
