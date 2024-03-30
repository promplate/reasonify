<script lang="ts">
  import type { PyAction } from ".";

  import Highlight from "../Highlight.svelte";
  import Hr from "./Hr.svelte";

  export let action: PyAction;
</script>

<div class="flex flex-col justify-between gap-2.5">
  <Highlight lang="python" theme="vitesse-dark" source={action.payload.source} />

  {#if action.payload.requirements && action.payload.source}
    <Hr />
  {/if}

  {#if action.payload.requirements}
    <div class="flex flex-row select-none items-center gap-1 text-xs text-lime-2 font-mono">
      <span>requirements:</span>
      <ul class="flex flex-row items-start gap-2.5">
        {#each action.payload.requirements as requirement}
          <li>
            <a href="https://pypi.org/project/{requirement}/" target="_blank" class="rounded bg-lime-2/10 px-1 py-0.5 hover:bg-lime-2/15">{requirement}</a>
          </li>
        {/each}
      </ul>
    </div>
  {/if}

  {#if action.result}
    {@const { "stdout/stderr": s, return: r, "global values": g } = action.result}
    {#if s}
      <Hr />
      <Highlight lang="ansi" theme="vitesse-dark" source={s.trimEnd()} />
    {/if}
    {#if g || r}
      <Hr />
      <Highlight lang="json" theme="vitesse-dark" source={JSON.stringify({ return: r, ...g }, null, 2)} />
    {/if}
  {/if}
</div>
