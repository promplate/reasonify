import extractorSvelte from "@unocss/extractor-svelte";
import { defineConfig, presetIcons, presetTypography, presetWebFonts, presetWind3, transformerDirectives, transformerVariantGroup } from "unocss";

const config = defineConfig({
  extractors: [extractorSvelte()],
  transformers: [transformerVariantGroup(), transformerDirectives()],
  presets: [presetWind3({ preflight: "on-demand" }), presetWebFonts({ provider: "bunny", fonts: {
    mono: { name: "JetBrains Mono Variable", provider: "none" },
    fira: { name: "Fira Code Variable", provider: "none" },
    fancy: "Archivo Black",
  } }), presetIcons(), presetTypography()],
});

export default config;
