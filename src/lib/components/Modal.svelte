<script lang="ts">
  export let show: boolean;

  let display = show;

  let timeoutId: ReturnType<typeof setTimeout>;

  $: if (show) {
    display = true;
    clearTimeout(timeoutId);
  } else {
    timeoutId = setTimeout(() => {
      display = false;
    }, 700);
  }
</script>

{#if display}
  <slot name="backdrop">
    <div class="fixed inset-0 transition duration-600" class:show />
  </slot>
  <div class="fixed inset-0 grid place-items-center transition duration-300" class:op-0={!show}>
    <slot name="inner">
      <div class="rounded bg-white/2 p-4 ring-1.3 ring-white/20">
        <slot />
      </div>
    </slot>
  </div>
{/if}

<style>
  div.show {
    --uno: bg-neutral-9/50 pointer-events-none;
  }
</style>
