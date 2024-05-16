<script>
  import "@unocss/reset/tailwind-compat.css";
  import "uno.css";

  import { Toaster } from "svelte-sonner";
</script>

<Toaster theme="dark" richColors position="bottom-left" toastOptions={{ class: "ws-pre-wrap font-mono" }} />

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
