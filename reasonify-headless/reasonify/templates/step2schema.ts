export type Output = {
  plan: string;
  tools: string[]; // tool ids, not tool names. This should not be empty!
} | {
  direct_response: string; // only when no tool helps!
};
