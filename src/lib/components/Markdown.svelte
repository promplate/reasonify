<script lang="ts">
  import type { BundledLanguage, BundledTheme } from "shiki";

  import "./md.css";

  import rehypeShiki from "@shikijs/rehype";
  import { cached } from "$lib/utils/cache";
  import rehypeStringify from "rehype-stringify";
  import remarkGfm from "remark-gfm";
  import remarkParse from "remark-parse";
  import remarkRehype from "remark-rehype";
  import { unified } from "unified";

  export let langs: BundledLanguage[] = [];
  export let text: string;
  export let theme: BundledTheme = "vitesse-dark";

  export async function renderMarkdown(text: string, langs: BundledLanguage[] = []) {
    const processor = cached(langs.join() + theme)(() => unified().use(remarkParse).use(remarkGfm).use(remarkRehype).use(rehypeShiki, { theme, langs }).use(rehypeStringify))();
    const { value } = await processor.process(text);
    return value as string;
  }

  let html = "";

  $: renderMarkdown(text, langs).then((out) => (html = out));
</script>

<div class="max-w-full prose [&>*:first-child]:mt-0 [&>*:last-child]:mb-0 [&>pre]:line-height-snug">
  {@html html}
</div>
