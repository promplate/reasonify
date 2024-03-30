import antfu from "@antfu/eslint-config";

export default antfu({
  svelte: true,
  typescript: true,
  stylistic: {
    quotes: "double",
    semi: true,
  },
  formatters: true,
  unocss: true,
  rules: {
    "perfectionist/sort-imports": ["error", {
      groups: ["type", ["side-effect", "side-effect-style"]],
    }],
    "import/order": "off",
    "node/prefer-global/process": "off",
    "svelte/no-at-html-tags": "off",
    "style/arrow-parens": "off",
    "style/brace-style": ["error", "1tbs"],
    "ts/no-use-before-define": "off",
    "no-alert": "warn",
    "no-console": "warn",
  },
});
