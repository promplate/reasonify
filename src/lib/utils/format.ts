export function formatSchemaPrompt(schema: string) {
  return `\`\`\`ts\n${schema.replaceAll("export ", "")}\n\`\`\``;
}
