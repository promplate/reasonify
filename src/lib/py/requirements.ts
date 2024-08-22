import code from "$lib/../../pyproject.toml?raw";

function getDependencies(toml: string) {
  return JSON.parse(/dependencies\s*=\s*(\[[\s\S]*?\])\n/.exec(toml)![1].replace(",\n]", "]")) as string[];
}

export default getDependencies(code);
