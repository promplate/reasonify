<script lang="ts">
  import Qr from "./QR.svelte";
  import { Pane, PaneGroup, PaneResizer } from "paneforge";
</script>

<div class="h-screen w-screen">
  <PaneGroup direction="horizontal">
    <Pane minSize={10} defaultSize={20}>
      <div class="h-full w-full flex flex-col select-none gap-5 ws-nowrap p-5">
        <div class="flex flex-col items-center gap-2 rounded-md bg-white/4 p-3 not-hover:op-80">
          <Qr url="/" scale={2} />
          <h3>扫码体验 Python Agent 🤖</h3>
        </div>
        <div class="flex flex-col items-center gap-2 rounded-md bg-white/4 p-3 not-hover:op-80">
          <Qr url="https://github.com/promplate/reasonify" scale={2} />
          <h3>GitHub 仓库求 ⭐</h3>
        </div>
        <div class="flex flex-row gap-2">
          <div class="flex flex-col items-center gap-2 rounded-md bg-white/4 p-3 not-hover:op-80">
            <Qr url="https://promplate.dev/" />
            <h3>体验提示工程框架</h3>
          </div>
          <div class="flex flex-col items-center gap-2 rounded-md bg-white/4 p-3 not-hover:op-80">
            <Qr url="https://docs.py.promplate.dev/" />
            <h3>提示工程框架文档</h3>
          </div>
        </div>
      </div>
    </Pane>
    <PaneResizer class="group">
      <div
        class="mx-1 h-full w-0.11em bg-white/10 transition group-active:bg-current group-hover:bg-white/30"
      />
    </PaneResizer>
    <Pane minSize={20}>
      <iframe class="h-full w-full" title="demo" src="/" frameborder="0" />
    </Pane>
  </PaneGroup>
</div>
