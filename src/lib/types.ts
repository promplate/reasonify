export type Role = "user" | "assistant" | "system";

export interface Message {
  role: Role;
  content: string;
  name?: string;
}

interface Snapshot {
  sources?: string[];
  results?: {
    "global values"?: string;
    "return"?: string;
    "stdout/stderr"?: string;
  }[];
  response?: string[];
  index?: number;
}

export interface Context {
  messages: Message[];
  snapshots?: Snapshot[];
  result?: string;
}
