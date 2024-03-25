import type { RequestHandler } from "./$types";
import type { OpenAIError } from "openai/error.mjs";
import type { ChatCompletionCreateParams } from "openai/resources/index.mjs";

import { error, text } from "@sveltejs/kit";
import { env } from "$env/dynamic/private";
import { OpenAIStream } from "ai";
import OpenAI from "openai";

const openai = new OpenAI({
  apiKey: env.OPENAI_API_KEY ?? "",
  baseURL: env.OPENAI_BASE_URL,
});

export const POST = (async ({ request }) => {
  const data: ChatCompletionCreateParams = await request.json();
  data.model = "gpt-3.5-turbo-0125";
  console.log(data);
  const headers = { "content-type": data?.response_format?.type === "json_object" ? "application/json" : "text/markdown; charset=utf-8" };
  try {
    if (data.stream) {
      const res = await openai.chat.completions.create(data);
      const stream = OpenAIStream(res);
      return new Response(stream, { headers });
    }
    else {
      const res = await openai.chat.completions.create(data);
      return text(res.choices[0].message.content ?? "", { headers });
    }
  }
  catch (err) {
    console.error(err);
    error((err as { status?: number }).status ?? 400, err as OpenAIError);
  }
}) satisfies RequestHandler;
