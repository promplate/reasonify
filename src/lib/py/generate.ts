import type { PyProxyTo } from "./common";
import type { ChatOptions } from "@xsai/shared-chat";
import type { Message } from "$lib/types";

import { toJs } from "./common";
import getGlobals from "./globals";
import chat from "$lib/chat";

const getEnsure = getGlobals<(prompt: string) => PyProxyTo<Message[]>>("parse_chat_markup", "from promplate import parse_chat_markup");

export default async function* async(prompt: string, kwargs: PyProxyTo<Omit<ChatOptions, "messages">>) {
  const options = toJs(kwargs);
  const ensure = await getEnsure();
  yield* chat({ ...options, messages: toJs(ensure(prompt)), stream: true });
}
