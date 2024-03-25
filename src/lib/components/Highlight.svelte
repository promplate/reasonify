<script lang="ts">
  import { cached } from "$lib/utils/cache";
  import { type BundledLanguage, type BundledTheme, getHighlighter } from "shiki";

  export let lang: BundledLanguage;
  export let source: string;
  export let theme: BundledTheme = "material-theme-ocean";

  async function highlight(source: string) {
    const highlighter = await cached(lang + theme)(() => getHighlighter({ langs: [lang], themes: [theme] }))();

    return highlighter.codeToHtml(source, { lang, theme });
  }

  let html = "";

  $: highlight(source).then((out) => (html = out));
</script>

<div>
  {@html html}
</div>

<style>
  div > :global(pre) {
    --uno: \!bg-transparent;
  }
</style>
