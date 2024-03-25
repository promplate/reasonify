<script lang="ts">
  import type { BundledLanguage, BundledTheme } from "shiki";

  import rehypeShiki from "@shikijs/rehype";
  import { cached } from "$lib/utils/cache";
  import rehypeStringify from "rehype-stringify";
  import remarkParse from "remark-parse";
  import remarkRehype from "remark-rehype";
  import { unified } from "unified";

  export const langs: BundledLanguage[] = [];
  export let text: string;
  export let theme: BundledTheme = "material-theme-ocean";

  export async function renderMarkdown(text: string, langs: BundledLanguage[] = []) {
    const processor = cached(langs.join() + theme)(() => unified().use(remarkParse).use(remarkRehype).use(rehypeShiki, { theme, langs }).use(rehypeStringify))();
    const { value } = await processor.process(text);
    return value as string;
  }

  let html = "";

  $: renderMarkdown(text).then((out) => (html = out));
</script>

<div class="max-w-full prose [&>*:first-child]:mt-0 [&>*:last-child]:mb-0">
  {@html html}
</div>
