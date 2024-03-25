import type { Tool } from "$lib/tools";

export interface Step1 {
  step: "step1";
  response?: string;
  tools: Tool[];
}

export interface Step2 {
  step: "step2";
  plan: string;
  tools: Tool[];
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
