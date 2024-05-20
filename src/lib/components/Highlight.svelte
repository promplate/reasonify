<script lang="ts">
  import { cached } from "$lib/utils/cache";
  import { type BundledLanguage, type BundledTheme, getHighlighter } from "shiki";

  export let lang: BundledLanguage | "ansi" | "text";
  export let source: string;
  export let theme: BundledTheme = "vesper";

  async function highlight(source: string) {
    const highlighter = await cached(lang + theme)(() => getHighlighter({ langs: [lang], themes: [theme] }))();

    return highlighter.codeToHtml(source, { lang, theme });
  }

  let html = "";

  $: highlight(source).then((out) => (html = out));
</script>

<div class="text-xs line-height-relaxed [&_*]:font-mono">
  {@html html}
</div>

<style>
  div > :global(pre) {
    --uno: \!bg-transparent;
  }
</style>
