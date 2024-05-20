<script>
  import "@unocss/reset/tailwind-compat.css";
  import "@fontsource-variable/jetbrains-mono";
  import "@fontsource-variable/fira-code";
  import "uno.css";

  import { emoji } from "$lib/stores";
  import { Toaster } from "svelte-sonner";
</script>

<svelte:head>
  <link rel="icon" href="https://api.iconify.design/fluent-emoji:{$emoji ?? "sparkler"}.svg" />
</svelte:head>

<Toaster theme="dark" richColors position="bottom-left" toastOptions={{ class: "ws-pre-wrap font-fira" }} />

<slot />

<style>
  :global(html) {
    --uno: bg-neutral-9 text-white flex flex-col items-center overflow-x-hidden;
  }

  :global(*)::selection {
    --uno: bg-white/15;
  }

  :global(body)::-webkit-scrollbar {
    --uno: bg-neutral-9 w-1 sm-w-1.5 md-w-2 lg-w-2.5 xl-w-3 2xl-w-3.5;
  }

  :global(body)::-webkit-scrollbar-thumb {
    --uno: bg-neutral-7/30 hover-bg-neutral-7/70 rounded-l-sm;
  }

  :global(body *)::-webkit-scrollbar {
    --uno: hidden;
  }
</style>
