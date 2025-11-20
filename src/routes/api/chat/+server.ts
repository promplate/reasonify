import type { RequestHandler } from "./$types";
import type { XSAIError } from "@xsai/shared";
import type { ChatOptions } from "@xsai/shared-chat";

import { error, text } from "@sveltejs/kit";
import { generateText } from "@xsai/generate-text";
import { streamText } from "@xsai/stream-text";
import { env } from "$env/dynamic/private";
import { createFetch } from "xsfetch";

const apiParams = {
  apiKey: env.OPENAI_API_KEY ?? "",
  baseURL: env.OPENAI_BASE_URL ?? "https://api.openai.com/v1",
};

const fetch = createFetch({ debug: true, retryDelay: 0 });

export const POST = (async ({ request }) => {
  const { stream, ...data } = await request.json() as ChatOptions & { stream: boolean; response_format?: { type: string } };
  data.model = "gpt-4o-mini";
  console.log(data);
  const headers = { "content-type": data?.response_format?.type?.includes("json") ? "application/json" : "text/markdown; charset=utf-8" };
  try {
    if (stream) {
      const { textStream } = await streamText({ ...data, ...apiParams, fetch });
      return new Response(textStream.pipeThrough(new TextEncoderStream()), { headers });
    } else {
      const res = await generateText({ ...data, ...apiParams, fetch });
      return text(res.text ?? "", { headers });
    }
  } catch (err) {
    console.error(err);
    error((err as { status?: number }).status ?? 400, err as XSAIError);
  }
}) satisfies RequestHandler;

export const config = { runtime: "edge" };
