<script lang="ts">
  import type { PyodideInterface } from "pyodide";

  import LoadingItem from "./LoadingItem.svelte";
  import getPy from "$lib/py";
  import { promplateReady, pyodideReady, reasonifyReady } from "$lib/stores";
  import { onMount } from "svelte";

  let py: PyodideInterface;

  onMount(async () => {
    py = await getPy();
  });
</script>

<ol class="fixed top-1/2 flex flex-col gap-2.5 -translate-1/2">
  <li><LoadingItem loading={!$pyodideReady} text="Loading pyodide runtime" /></li>
  <li class:op-30={!$pyodideReady}><LoadingItem loading={!$promplateReady} text="Patching promplate" /></li>
  <li class:op-30={!$promplateReady}><LoadingItem loading={!$reasonifyReady} text="Building headless agent" /></li>
</ol>
