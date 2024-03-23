interface FinishOutput {
  action: "finish";
  message: string;
}

interface ContinueOutput {
  action: "continue";
  next_step: {
    plan: string;
    tools: string[]; // tool ids, not tool names. This should not be empty!
  };
}

export type Output = FinishOutput | ContinueOutput;
