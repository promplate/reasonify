<script lang="ts">
  import Chat from "../lib/components/Chat.svelte";
  import LoadingItem from "./LoadingItem.svelte";
  import { browser } from "$app/environment";
  import Modal from "$lib/components/Modal.svelte";
  import { getChain } from "$lib/py";
  import { promplateReady, pyodideReady, reasonifyReady } from "$lib/stores";
</script>

{#if browser}
  {#await getChain() then chain}
    <Chat {chain} />
  {/await}
{/if}

<Modal show={!$reasonifyReady}>
  <ol class="flex flex-col gap-2.5 whitespace-nowrap">
    <li><LoadingItem loading={!$pyodideReady} text="Loading pyodide runtime" /></li>
    <li class:op-30={!$pyodideReady}><LoadingItem loading={!$promplateReady} text="Patching promplate" /></li>
    <li class:op-30={!$promplateReady}><LoadingItem loading={!$reasonifyReady} text="Building headless agent" /></li>
  </ol>
</Modal>
