import type { Tool } from "..";

import schema from "./schema.ts?raw";
import { formatSchemaPrompt } from "$lib/utils/format";

export default {
  id: "clarify",
  name: "Ask for clarification",
  usage: "The user don't know much, you can only ask the user for his/her personal information. WARNING: only use this when other approaches all failed. Never use this first.",
  schema: formatSchemaPrompt(schema),
  instruction: "Your prompt must be in the same language as the user's query.",
  async run({ question }) {
    return { answer: prompt(question as string) };
  },
} as Tool;
