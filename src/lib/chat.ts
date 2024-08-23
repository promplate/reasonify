import type { ChatCompletionCreateParams } from "openai/resources/index";

import { responseToAsyncIterator } from "./utils/iter";

export default async function* (options: ChatCompletionCreateParams) {
  const res = await fetch("/api/chat", { method: "POST", body: JSON.stringify(options), headers: { "content-type": "application/json" } });
  if (res.status !== 200) {
    console.error(await res.text());
    throw new Error(`Failed to fetch: ${res.status} ${res.statusText}`);
  }
  yield * responseToAsyncIterator(res);
}
