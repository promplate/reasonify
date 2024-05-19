<script lang="ts">
  import Chat from "../lib/components/Chat.svelte";
  import LoadingItem from "./LoadingItem.svelte";
  import { browser } from "$app/environment";
  import Modal from "$lib/components/Modal.svelte";
  import { initChain } from "$lib/py";
  import reasonifyVersion from "$lib/py/version";
  import { pyodideReady, reasonifyReady } from "$lib/stores";
  import { version as pyodideVersion } from "pyodide";

</script>

{#if browser}
  {#await initChain() then chain}
    <Chat {chain} />
  {/await}
{/if}

<Modal show={!$reasonifyReady}>
  <ol class="flex flex-col gap-2.5 whitespace-nowrap">
    <li><LoadingItem loading={!$pyodideReady} text="Loading pyodide v{pyodideVersion}" /></li>
    <li class:op-30={!$pyodideReady}><LoadingItem loading={!$reasonifyReady} text="Loading reasonify v{reasonifyVersion}" /></li>
  </ol>
</Modal>
