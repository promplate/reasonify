import type { Tool } from "$lib/tools";
import type { Output } from "$lib/tools/python/schema";

export interface Step2 {
  step: "step2";
  plan: string;
  tools: Tool[];
  direct_response?: string;
}

interface Action {
  purpose: string;
  payload: object;
  result?: object;
  tool_id: string;
  tool?: Tool;
}

export interface PyAction extends Action {
  tool_id: "py";
  payload: {
    source: string;
    requirements?: string[];
  };
  result: Output;
}

interface AskAction extends Action {
  tool_id: "clarify";
  payload: {
    question: string;
  };
}

export interface Step3 {
  step: "step3";
  note: string;
  actions: (AskAction | PyAction)[];
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
