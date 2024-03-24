<script lang="ts">
  import LoadingItem from "./LoadingItem.svelte";
  import Modal from "$lib/components/Modal.svelte";
  import getPy from "$lib/py";
  import { promplateReady, pyodideReady, reasonifyReady } from "$lib/stores";
  import { onMount } from "svelte";

  onMount(() => void getPy());
</script>

<Modal show={!$reasonifyReady}>
  <ol class="flex flex-col gap-2.5 whitespace-nowrap">
    <li><LoadingItem loading={!$pyodideReady} text="Loading pyodide runtime" /></li>
    <li class:op-30={!$pyodideReady}><LoadingItem loading={!$promplateReady} text="Patching promplate" /></li>
    <li class:op-30={!$promplateReady}><LoadingItem loading={!$reasonifyReady} text="Building headless agent" /></li>
  </ol>
</Modal>
