import { sveltekit } from "@sveltejs/kit/vite";
import flattenDir from "rollup-plugin-flatten-dir";
import Unocss from "unocss/vite";
import { defineConfig } from "vite";

export default defineConfig({
  plugins: [Unocss(), sveltekit(), flattenDir()],
  optimizeDeps: { entries: ["index.html", "**/*.svelte", "src/routes/**/*.ts", "!**/*server.ts"] },
});
