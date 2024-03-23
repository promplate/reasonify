<script lang="ts">
  export let text: string;
  export let loading: boolean;
</script>

<div class="flex flex-row items-center gap-2">
  <div class={loading ? "i-svg-spinners-90-ring-with-bg op-70" : "i-lucide-check"}></div>
  <div class="text-3.9">{text}</div>
</div>
