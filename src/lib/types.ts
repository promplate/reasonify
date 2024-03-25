import type { Step1, Step2, Step3, Step4 } from "./components/snapshots";
import type { Tool } from "./tools";

export type Role = "user" | "assistant" | "system";

export interface Message {
  role: Role;
  content: string;
  name?: string;
}

export interface Context {
  messages: Message[];
  all_tools: Tool[];

  result?: string;
  snapshots?: (Step1 | Step2 | Step3 | Step4)[];
}
