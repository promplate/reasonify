<script lang="ts">
  // @ts-ignore
  import QRious from "qrious";
  import { onMount } from "svelte";

  export let url: string;
  export let scale = 1;

  let qr: QRious;

  onMount(() => {
    qr = new QRious({
      value: new URL(url, location.href).href,
      background: "#00000000",
      foreground: "#ffffff",
      size: 345 * scale,
      level: ["L", "M", "Q", "H"][scale],
    });
  });
</script>

<img src={qr?.toDataURL("image/svg")} alt="qr code" />
