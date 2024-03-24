import type { Tool } from "..";

import schema from "./schema.ts?raw";
import { formatSchemaPrompt } from "$lib/utils/format";

export default {
  id: "ask",
  name: "Ask the user",
  usage: "Ask the user for input. The user's response will be the tool's output.",
  schema: formatSchemaPrompt(schema),
  async run({ question }) {
    return { answer: prompt(question as string) };
  },
} as Tool;
