import type { Tool } from "$lib/tools";

export interface Step2 {
  step: "step2";
  plan: string;
  tools: Tool[];
  direct_response?: string;
}

export interface Step3 {
  step: "step3";
  note: string;
  actions: {
    purpose: string;
    payload: object;
    result?: object;
    tool_id: string;
    tool?: Tool;
  }[];
}

export interface Step4 {
  step: "step4";
  action: "finish" | "continue";
  message?: string;
  summary: string;
  next_step?: {
    plan: string;
    tools: string[];
  };
}
